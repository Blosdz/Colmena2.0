import { Activity, BarChart3, FileCheck2, Home, Plus } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';

import { cn } from '../../utils/cn.js';
import { getActiveProjectId } from '../../utils/activeProject.js';

export function CompanyMobileNav() {
  const location = useLocation();
  const match = location.pathname.match(/^\/colmena\/project\/([a-zA-Z0-9-]+)/);
  const projectId = match?.[1] || getActiveProjectId();
  const links = [
    ['/colmena', 'Inicio', Home],
    ['/colmena/campaign/new?instrument=MEDIUM', 'Nueva', Plus],
    [projectId ? `/colmena/project/${projectId}/telemetry` : '/colmena', 'Captura', Activity],
    [projectId ? `/colmena/project/${projectId}/results` : '/colmena', 'Resultados', BarChart3],
    [projectId ? `/colmena/project/${projectId}/reports` : '/colmena', 'Reporte', FileCheck2],
  ];
  return <nav aria-label="Navegaci?n m?vil" className="fixed inset-x-3 bottom-3 z-50 grid grid-cols-5 rounded-2xl border border-white/60 bg-white/88 p-1.5 shadow-[0_20px_60px_rgba(15,45,49,.22)] backdrop-blur-2xl lg:hidden">{links.map(([to, label, Icon]) => { const active = location.pathname === to.split('?')[0] || (label !== 'Inicio' && location.pathname.startsWith(to.split('?')[0])); return <Link key={label} to={to} className={cn('flex min-w-0 flex-col items-center gap-1 rounded-xl px-1 py-2 text-[9px] font-bold text-muted', active && 'bg-[#16383d] text-white')}><Icon size={16} /><span className="truncate">{label}</span></Link>; })}</nav>;
}

export default CompanyMobileNav;
