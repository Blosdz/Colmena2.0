import { useQuery } from '@tanstack/react-query';
import {
  Activity,
  Archive,
  BarChart3,
  Building2,
  ChevronDown,
  ClipboardCheck,
  FileCheck2,
  Gauge,
  Home,
  LayoutDashboard,
  ListChecks,
  Plus,
  ShieldCheck,
} from 'lucide-react';
import { Link, useLocation, useNavigate } from 'react-router-dom';

import { listProjects } from '../../api/projects.js';
import { BrandLogo } from '../../brand/BrandLogo.jsx';
import { cn } from '../../utils/cn.js';
import { getActiveProjectId, setActiveProjectId } from '../../utils/activeProject.js';
import { ColmenaMenuButton } from './ColmenaMenuButton.jsx';

function NavLink({ to, icon: Icon, label, active, badge }) {
  return <Link to={to} className={cn('group flex h-10 items-center gap-3 rounded-xl px-3 text-[13px] font-semibold transition', active ? 'bg-gradient-to-r from-amber/14 to-amber/5 text-dark ring-1 ring-amber/15' : 'text-muted hover:bg-[#f3f6f6] hover:text-dark')}><Icon className={cn('h-[17px] w-[17px] shrink-0', active ? 'text-amber' : 'text-muted/55 group-hover:text-turquoise')} strokeWidth={active ? 2.3 : 1.8} /><span className="min-w-0 flex-1 truncate">{label}</span>{badge ? <span className="rounded-full bg-turquoise/10 px-1.5 py-0.5 text-[8px] font-black text-turquoise">{badge}</span> : null}</Link>;
}

export function CompanySidebar({ collapsed = false, onToggle }) {
  const location = useLocation();
  const navigate = useNavigate();
  const match = location.pathname.match(/^\/colmena\/project\/([a-zA-Z0-9-]+)/);
  const routeProjectId = match ? match[1] : null;
  const activeProjectId = routeProjectId && routeProjectId !== 'new' ? routeProjectId : getActiveProjectId();
  const hasProject = Boolean(activeProjectId && activeProjectId !== 'new');
  const projectsQuery = useQuery({ queryKey: ['sidebar-projects'], queryFn: () => listProjects({ page: 1, pageSize: 100 }) });
  const campaigns = (projectsQuery.data?.items || []).filter((project) => project.project_type === 'CENSO');

  const selectCampaign = (event) => {
    const projectId = event.target.value;
    if (!projectId) return;
    setActiveProjectId(projectId);
    navigate(`/colmena/project/${projectId}`);
  };

  const path = location.pathname;
  const campaignPath = (suffix = '') => hasProject ? `/colmena/project/${activeProjectId}${suffix}` : '/colmena';

  return (
    <aside className={cn('hidden shrink-0 overflow-hidden transition-[width] duration-200 lg:block', collapsed ? 'lg:w-0' : 'lg:w-[252px]')}>
      <div className={cn('sticky top-0 flex h-screen w-[252px] flex-col border-r border-white/60 bg-white/84 shadow-[14px_0_45px_rgba(26,55,58,.035)] backdrop-blur-2xl transition-opacity', collapsed && 'pointer-events-none opacity-0')}>
        <div className="px-5 pb-4 pt-5"><div className="flex items-start justify-between gap-2"><BrandLogo /><ColmenaMenuButton onClick={() => onToggle?.()} title="Contraer men?" className="mt-0.5 rounded-lg p-1.5 hover:bg-[#f5f7f7]" /></div><div className="mt-3 flex items-center gap-2 rounded-xl bg-[#12363a] px-3 py-2 text-white"><ShieldCheck size={14} className="text-[#8fe4dd]" /><div><p className="text-[10px] font-extrabold uppercase tracking-wider">Empresa</p><p className="text-[9px] text-white/50">Evaluaci?n psicosocial</p></div></div></div>

        <nav className="flex-1 space-y-6 overflow-y-auto px-3 py-3">
          <div className="space-y-1">
            <NavLink to="/colmena" icon={Home} label="Centro de instrumentos" active={path === '/colmena'} />
            <NavLink to="/colmena/campaign/new?instrument=MEDIUM" icon={Plus} label="Nueva evaluaci?n" active={path.includes('/campaign/new')} badge="NUEVO" />
            <NavLink to="/colmena/company" icon={Building2} label="Datos de la empresa" active={path === '/colmena/company'} />
          </div>

          <div>
            <p className="mb-2 px-3 text-[9px] font-black uppercase tracking-[.14em] text-muted/45">Campa?a activa</p>
            <div className="relative mb-3"><ClipboardCheck className="pointer-events-none absolute left-3 top-3 h-4 w-4 text-turquoise" /><select value={hasProject ? activeProjectId : ''} onChange={selectCampaign} className="h-10 w-full appearance-none rounded-xl border border-border bg-white pl-9 pr-8 text-[11px] font-bold text-dark outline-none focus:border-turquoise" disabled={!campaigns.length}><option value="">Selecciona una campa?a</option>{campaigns.map((project) => <option key={project.id} value={project.id}>{project.name}</option>)}</select><ChevronDown className="pointer-events-none absolute right-3 top-3 h-4 w-4 text-muted" /></div>
            <div className={cn('space-y-1', !hasProject && 'pointer-events-none opacity-40')}>
              <NavLink to={campaignPath()} icon={LayoutDashboard} label="Resumen de campa?a" active={hasProject && path === campaignPath()} />
              <NavLink to={campaignPath('/form')} icon={ListChecks} label="Instrumento" active={path.includes('/form')} />
              <NavLink to={campaignPath('/telemetry')} icon={Activity} label="Telemetr?a" active={path.includes('/telemetry') || path.includes('/link')} />
              <NavLink to={campaignPath('/results')} icon={BarChart3} label="Dashboard anal?tico" active={path.includes('/results') || path.includes('/premium')} />
              <NavLink to={campaignPath('/analysis')} icon={Gauge} label="Laboratorio estad?stico" active={path.includes('/analysis')} />
              <NavLink to={campaignPath('/reports')} icon={FileCheck2} label="Expediente t?cnico" active={path.includes('/reports')} />
            </div>
          </div>

          <div><p className="mb-2 px-3 text-[9px] font-black uppercase tracking-[.14em] text-muted/45">Hist?rico</p><NavLink to="/colmena/archive/projects" icon={Archive} label="Evaluaciones anteriores" active={path.includes('/archive')} /></div>
        </nav>

        <div className="m-3 rounded-2xl border border-turquoise/15 bg-gradient-to-br from-turquoise/8 to-amber/6 p-3"><div className="flex items-center gap-2"><span className="flex h-8 w-8 items-center justify-center rounded-xl bg-white text-turquoise shadow-sm"><Gauge size={15} /></span><div><p className="text-[11px] font-black text-dark">Colmena Intelligence</p><p className="text-[9px] text-muted">Motor estad?stico trazable</p></div></div></div>
      </div>
    </aside>
  );
}

export default CompanySidebar;
