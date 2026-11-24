"""Read-only ARC 01 checks. A PASS means inspection-ready, not live-test acceptance."""
import argparse
import json
import shutil
import socket
import subprocess
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit
from bridge_mcp import MCPError, validate_endpoint
from configure import matching_servers
from unreal_session import UnrealSession

PLUGIN_PATHS = {
    'ModelContextProtocol':'Engine/Plugins/Experimental/ModelContextProtocol/ModelContextProtocol.uplugin',
    'AllToolsets':'Engine/Plugins/Experimental/Toolsets/AllToolsets/AllToolsets.uplugin',
    'ToolsetRegistry':'Engine/Plugins/Experimental/ToolsetRegistry/ToolsetRegistry.uplugin',
}


def check_engine(engine):
    build = engine/'Engine/Build/Build.version'
    if not build.is_file(): raise ValueError('Engine Build.version missing; finish installing UE 5.8')
    version=json.loads(build.read_text(encoding='utf-8-sig'))
    if (version.get('MajorVersion'),version.get('MinorVersion'))!=(5,8):
        raise ValueError('This ARC targets Unreal Engine 5.8 only')
    has_win_exe = (engine/'Engine/Binaries/Win64/UnrealEditor.exe').is_file()
    has_mac_exe = (engine/'Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor').is_file()
    if sys.platform == 'darwin':
        if not has_mac_exe and not has_win_exe:
            raise ValueError('UnrealEditor executable is missing on macOS')
    else:
        if not has_win_exe and not has_mac_exe:
            raise ValueError('UnrealEditor.exe is missing')
    for name,path in PLUGIN_PATHS.items():
        if not (engine/path).is_file(): raise ValueError('Missing required native plugin: '+name)
        json.loads((engine/path).read_text(encoding='utf-8-sig'))
    return version


def resolve_agy_bin():
    """Resolve Google Antigravity CLI ('agy') executable safely across platforms."""
    if sys.platform == 'win32':
        resolved = shutil.which('agy.cmd') or shutil.which('agy.exe') or shutil.which('agy')
    else:
        resolved = shutil.which('agy')
    if not resolved:
        gemini_bin = Path.home() / '.gemini' / 'bin' / ('agy.exe' if sys.platform == 'win32' else 'agy')
        if gemini_bin.is_file():
            resolved = str(gemini_bin)
    if not resolved:
        raise ValueError("Google Antigravity CLI ('agy') absent from PATH and ~/.gemini/bin")
    return resolved


def resolve_codex_bin():
    """Resolve Codex CLI executable safely across Windows, Linux, and macOS (compatibility fallback)."""
    if sys.platform == 'win32':
        resolved = shutil.which('codex.cmd') or shutil.which('codex.exe') or shutil.which('codex')
    else:
        resolved = shutil.which('codex')
    if not resolved:
        raise ValueError('Codex CLI absent from PATH')
    return resolved


def result_code(checks):
    statuses={c['status'] for c in checks}
    return 1 if 'FAIL' in statuses else 2 if statuses & {'BLOCKED','NOT TESTED'} else 0


def run(project, engine, endpoint, full=False):
    checks=[]
    report={'timestamp_utc':datetime.now(timezone.utc).isoformat(),'endpoint':endpoint,'checks':checks,
            'live_creation':'NOT TESTED: run scripts/live_test.py separately'}
    def check(name,action,missing='FAIL'):
        try:
            value=action();checks.append({'name':name,'status':'PASS','detail':value});return value
        except (OSError,ValueError,RuntimeError,subprocess.SubprocessError) as exc:
            checks.append({'name':name,'status':missing,'detail':str(exc)});return None
    check('python',lambda:sys.version)
    def cli():
        try:
            bin_path = resolve_agy_bin()
            out = subprocess.check_output([bin_path, '--version'], text=True, timeout=15).strip()
            return f"Antigravity CLI: {out} ({bin_path})"
        except Exception:
            try:
                codex_bin = resolve_codex_bin()
                out = subprocess.check_output([codex_bin, '--version'], text=True, timeout=15).strip()
                return f"Codex CLI (fallback): {out} ({codex_bin})"
            except Exception:
                raise ValueError("Neither Google Antigravity CLI ('agy') nor compatible AI client found")
    check('antigravity_cli',cli,'BLOCKED')
    def project_check():
        if not project or not project.is_file() or project.suffix.lower()!='.uproject':
            raise ValueError('Supply the full path to an existing target .uproject')
        d=json.loads(project.read_text(encoding='utf-8-sig'))
        enabled={p['Name']:p.get('Enabled') for p in d.get('Plugins',[])}
        for name in ('ModelContextProtocol','AllToolsets'):
            if enabled.get(name) is not True: raise ValueError(name+' is not enabled')
        if enabled.get('ToolsetRegistry') is False: raise ValueError('ToolsetRegistry dependency explicitly disabled')
        return {'path':str(project),'plugins':enabled}
    project_data=check('project_and_plugins',project_check,'BLOCKED')
    version=check('engine',lambda:check_engine(engine),'BLOCKED')
    def config_check():
        if not project_data: raise ValueError('Project unavailable')
        # 1. Check Antigravity native mcp_config.json or project .mcp.json
        candidate_paths = [
            project.parent / 'mcp_config.json',
            project.parent / '.mcp.json',
            Path(__file__).resolve().parents[1] / 'mcp_config.json'
        ]
        for p in candidate_paths:
            if p.is_file():
                try:
                    data = json.loads(p.read_text(encoding='utf-8-sig'))
                    servers = data.get('mcpServers', {})
                    if 'unreal-mcp' in servers:
                        srv = servers['unreal-mcp']
                        srv_url = srv.get('url') or srv.get('serverUrl')
                        if srv_url == endpoint:
                            return {'path': str(p), 'server': 'unreal-mcp', 'url': srv_url, 'format': 'antigravity_mcp_config'}
                except Exception:
                    pass

        # 2. Check compatibility .codex/config.toml
        codex_path = project.parent / '.codex/config.toml'
        if codex_path.is_file():
            try:
                data = tomllib.loads(codex_path.read_text(encoding='utf-8-sig'))
                matches = matching_servers(data, endpoint)
                if len(matches) == 1:
                    return {'path': str(codex_path), 'server': matches[0], 'format': 'codex_toml'}
            except Exception:
                pass

        raise ValueError('Expected MCP registration for endpoint in mcp_config.json (or .mcp.json)')
    check('mcp_configuration',config_check,'BLOCKED')
    valid=check('loopback_endpoint',lambda:validate_endpoint(endpoint))
    def tcp():
        p=urlsplit(endpoint)
        with socket.create_connection((p.hostname,p.port or 80),timeout=3): return 'Reachable; not proof of MCP'
    if valid: check('tcp',tcp)
    session=UnrealSession(endpoint) if valid else None
    init=check('mcp_initialization_and_discovery',lambda:session.connect(full)) if session else None
    if init is not None:
        report['initialization']=init
        report['capabilities']=session.capability_report()
        report['toolset_names']=session.names
        identity=check('active_project_identity',lambda:session.verify_identity(project,engine)) if project_data and version else None
        if identity:
            report['identity']=identity
            check('current_level',lambda:session.invoke('SceneTools','get_current_level'))
            check('actor_listing',lambda:session.invoke('SceneTools','find_actors',name='',tag='',collision_channels=[]))
        else:
            checks.append({'name':'scene_inspection','status':'BLOCKED','detail':'Project identity was not verified'})
    else:
        checks.append({'name':'active_project_identity','status':'BLOCKED','detail':'No initialized MCP session'})
        checks.append({'name':'scene_inspection','status':'NOT TESTED','detail':'No initialized MCP session'})
    if session: report['transcript']=session.client.transcript
    report['exit_code']=result_code(checks)
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project',type=Path,required=True)
    parser.add_argument('--engine',type=Path,required=True)
    parser.add_argument('--endpoint',default='http://127.0.0.1:8000/mcp')
    parser.add_argument('--full',action='store_true',help='Describe all toolsets sequentially')
    parser.add_argument('--output',type=Path,default=Path('evidence/doctor.json'))
    args=parser.parse_args()
    report=run(args.project.resolve(),args.engine.resolve(),args.endpoint,args.full)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2),encoding='utf-8')
    for c in report['checks']:
        detail=c['detail']
        if c['name']=='actor_listing' and isinstance(detail,list): detail=f'{len(detail)} actors'
        print(c['status'],c['name'],str(detail)[:500])
    print('Evidence:',args.output.resolve())
    return report['exit_code']


if __name__=='__main__': raise SystemExit(main())
