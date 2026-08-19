import { useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import {
  Activity,
  ArrowRight,
  BarChart3,
  BookOpenCheck,
  Building2,
  CheckCircle2,
  ChevronRight,
  CircleDashed,
  ClipboardCheck,
  Clock3,
  FileCheck2,
  FlaskConical,
  HeartPulse,
  Layers3,
  LockKeyhole,
  Plus,
  ShieldCheck,
  Sparkles,
  Target,
  Users,
} from 'lucide-react';

import { getCompanyProfile } from '../../api/company.js';
import { listProjects } from '../../api/projects.js';
import { useAuth } from '../../auth/AuthContext.jsx';
import { Button } from '../../components/ui/Button.jsx';
import { Card } from '../../components/ui/Card.jsx';
import { ErrorState } from '../../components/ui/ErrorState.jsx';
import { LoadingState } from '../../components/ui/LoadingState.jsx';

const INSTRUMENTS = [
  {
    code: 'SHORT',
    title: 'CENSOPAS-COPSOQ corta',
    eyebrow: 'Diagnóstico por dimensiones',
    description: 'Aplicación ágil para centros pequeños o una lectura global de los seis dominios psicosociales.',
    questions: 42,
    scored: 31,
    output: '6 dimensiones',
    time: '8–12 min',
    icon: ClipboardCheck,
    accent: '#18a7a1',
    glow: 'from-[#0f766e]/15 to-[#d9f6f3]/30',
    recommended: '< 25 participantes efectivos',
  },
  {
    code: 'MEDIUM',
    title: 'CENSOPAS-COPSOQ media',
    eyebrow: 'Diagnóstico profundo',
    description: 'Lectura completa con subdimensiones, salud, bienestar y mayor capacidad de segmentación organizacional.',
    questions: 112,
    scored: 69,
    output: '6 dimensiones ? 20 subdimensiones',
    time: '18–25 min',
    icon: Layers3,
    accent: '#d59b27',
    glow: 'from-[#d59b27]/15 to-[#fff4cf]/45',
    recommended: '≥ 25 participantes efectivos',
  },
];

const FUTURE_INSTRUMENTS = [
  ['LISTAS', 'Evaluación de factores complementarios', BookOpenCheck],
  ['Salud ocupacional', 'Indicadores preventivos y vigilancia', HeartPulse],
  ['Clima de seguridad', 'Cultura, liderazgo y conductas seguras', ShieldCheck],
];

function Metric({ icon: Icon, label, value, detail, tone = 'dark' }) {
  const tones = {
    dark: 'bg-[#16383d] text-white',
    teal: 'bg-turquoise/12 text-turquoise',
    amber: 'bg-amber/15 text-yellowDark',
    green: 'bg-emerald-50 text-emerald-700',
  };
  return (
    <div className="rounded-2xl border border-white/65 bg-white/80 p-4 shadow-[0_12px_32px_rgba(24,52,56,.07)] backdrop-blur-xl">
      <div className="flex items-start justify-between gap-3"><span className={`flex h-9 w-9 items-center justify-center rounded-xl ${tones[tone]}`}><Icon size={17} /></span><span className="h-2 w-2 rounded-full bg-turquoise/70" /></div>
      <p className="mt-4 text-[10px] font-extrabold uppercase tracking-[0.12em] text-muted">{label}</p>
      <p className="mt-1 text-2xl font-black tracking-tight text-dark">{value}</p>
      <p className="mt-1 text-[11px] leading-4 text-muted">{detail}</p>
    </div>
  );
}

function InstrumentCard({ instrument, profileReady }) {
  const Icon = instrument.icon;
  return (
    <article className="group relative overflow-hidden rounded-[26px] border border-white/70 bg-white/82 p-5 shadow-[0_18px_50px_rgba(24,52,56,.08)] backdrop-blur-xl transition duration-300 hover:-translate-y-1 hover:shadow-[0_26px_70px_rgba(24,52,56,.14)] sm:p-6">
      <div className={`pointer-events-none absolute inset-0 bg-gradient-to-br ${instrument.glow} opacity-60`} />
      <div className="relative">
        <div className="flex items-start justify-between gap-4">
          <span className="flex h-12 w-12 items-center justify-center rounded-2xl text-white shadow-lg" style={{ background: instrument.accent }}><Icon size={22} /></span>
          <span className="rounded-full border border-white/70 bg-white/65 px-3 py-1 text-[10px] font-extrabold uppercase tracking-wider text-dark backdrop-blur">Disponible</span>
        </div>
        <p className="mt-5 text-[10px] font-extrabold uppercase tracking-[0.14em]" style={{ color: instrument.accent }}>{instrument.eyebrow}</p>
        <h2 className="mt-1 text-xl font-black tracking-tight text-dark">{instrument.title}</h2>
        <p className="mt-2 min-h-[60px] text-xs leading-5 text-muted">{instrument.description}</p>
        <div className="mt-5 grid grid-cols-3 gap-2">
          {[[instrument.questions, 'preguntas'], [instrument.scored, 'puntuables'], [instrument.time, 'duración']].map(([value, label]) => <div key={label} className="rounded-xl border border-white bg-white/60 p-3"><p className="text-sm font-black text-dark">{value}</p><p className="mt-0.5 text-[9px] font-bold uppercase tracking-wide text-muted">{label}</p></div>)}
        </div>
        <div className="mt-3 rounded-xl border border-dark/5 bg-dark/[.045] px-3 py-2.5">
          <p className="text-[11px] font-bold text-dark">{instrument.output}</p>
          <p className="mt-0.5 text-[10px] text-muted">Recomendado: {instrument.recommended}</p>
        </div>
        {profileReady ? (
          <Link to={`/colmena/campaign/new?instrument=${instrument.code}`} className="mt-5 flex h-11 w-full items-center justify-between rounded-xl bg-[#16383d] px-4 text-sm font-bold text-white transition hover:bg-[#0f2d31]">
            Configurar evaluación <ArrowRight size={16} className="transition group-hover:translate-x-1" />
          </Link>
        ) : (
          <Link to="/colmena/company" className="mt-5 flex h-11 w-full items-center justify-between rounded-xl bg-amber px-4 text-sm font-bold text-dark">Completar empresa <Building2 size={16} /></Link>
        )}
      </div>
    </article>
  );
}

function CampaignCard({ project }) {
  const metadata = project.metadata || {};
  const version = metadata.instrument_version_kind === 'SHORT' ? 'Corta' : 'Media';
  const hasCampaign = Boolean(metadata.demo_campaign);
  const status = hasCampaign ? 'EN CAMPO' : project.status === 'ACTIVE' ? 'CONFIGURACIÓN' : project.status;
  return (
    <article className="rounded-2xl border border-border bg-white p-4 shadow-sm transition hover:border-turquoise/35 hover:shadow-md">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div className="flex min-w-0 items-start gap-3"><span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-[#16383d] text-white"><Activity size={18} /></span><div className="min-w-0"><p className="truncate text-sm font-extrabold text-dark">{project.name}</p><p className="mt-1 text-[11px] text-muted">CENSOPAS {version} · {metadata.expected_worker_count || '—'} trabajadores</p></div></div>
        <span className={`rounded-full px-2.5 py-1 text-[9px] font-extrabold tracking-wider ${hasCampaign ? 'bg-emerald-50 text-emerald-700' : 'bg-amber/15 text-yellowDark'}`}>{status}</span>
      </div>
      <div className="mt-4 grid grid-cols-3 gap-2 text-center">
        {[[hasCampaign ? metadata.demo_campaign.synthetic_responses : 0, 'respuestas'], [metadata.min_publishable_n || 5, 'mínimo n'], [metadata.official_equivalence_enabled ? 'Sí' : 'Demo', 'equivalencia']].map(([value, label]) => <div key={label} className="rounded-xl bg-surfaceSoft px-2 py-2"><p className="text-sm font-black text-dark">{value}</p><p className="text-[9px] uppercase tracking-wide text-muted">{label}</p></div>)}
      </div>
      <div className="mt-4 flex items-center gap-2">
        <Link className="flex-1" to={`/colmena/project/${project.id}`}><Button className="w-full" size="sm" variant="secondary">Abrir campaña</Button></Link>
        {hasCampaign ? <Link to={`/colmena/project/${project.id}/results`}><Button size="sm"><BarChart3 size={14} /></Button></Link> : null}
      </div>
    </article>
  );
}

export default function CompanyDashboardPage() {
  const { user } = useAuth();
  const profileQuery = useQuery({ queryKey: ['company-profile'], queryFn: getCompanyProfile });
  const projectsQuery = useQuery({ queryKey: ['projects', { page: 1 }], queryFn: () => listProjects({ page: 1, pageSize: 50 }) });
  const projects = projectsQuery.data?.items || [];
  const campaigns = useMemo(() => projects.filter((project) => project.project_type === 'CENSO'), [projects]);
  const active = campaigns.filter((project) => project.metadata?.campaign_status === 'OPEN' || project.metadata?.demo_campaign).length;
  const profile = profileQuery.data;
  const profileReady = Boolean(profile?.tax_id && profile?.worker_count);

  if (profileQuery.isLoading || projectsQuery.isLoading) return <LoadingState label="Preparando el centro empresarial…" />;
  if (profileQuery.isError || projectsQuery.isError) return <ErrorState title="No pudimos abrir el centro empresarial" message={profileQuery.error?.message || projectsQuery.error?.message} />;

  return (
    <div className="colmena-page pb-16">
      <section className="relative overflow-hidden rounded-[30px] border border-white/15 bg-gradient-to-br from-[#0d2d31] via-[#153e42] to-[#17635f] p-6 text-white shadow-[0_30px_80px_rgba(16,47,51,.24)] sm:p-8 lg:p-10">
        <div className="absolute -right-20 -top-28 h-72 w-72 rounded-full bg-[#55d7cd]/15 blur-3xl" /><div className="absolute -bottom-36 left-1/3 h-64 w-64 rounded-full bg-amber/15 blur-3xl" />
        <div className="relative grid gap-8 xl:grid-cols-[1.35fr_.65fr] xl:items-end">
          <div>
            <div className="flex flex-wrap items-center gap-2"><span className="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/10 px-3 py-1.5 text-[10px] font-extrabold uppercase tracking-[0.16em] text-[#9ce8e4]"><Sparkles size={13} /> Centro de evaluación psicosocial</span><span className="rounded-full bg-amber px-3 py-1.5 text-[10px] font-black text-dark">DEMO SINTÉTICO</span></div>
            <p className="mt-5 text-xs font-semibold text-white/55">Hola, {user?.first_name || 'equipo SST'}</p>
            <h1 className="mt-1 max-w-3xl text-3xl font-black tracking-[-.035em] sm:text-4xl">{profile?.name || 'Configuremos primero tu empresa'}</h1>
            <p className="mt-4 max-w-2xl text-sm leading-6 text-white/68">Selecciona un instrumento, configura la población y publica una campaña anónima. Colmena transforma la captura en evidencia, decisiones preventivas y expediente técnico.</p>
            <div className="mt-6 flex flex-wrap gap-2">
              <a href="#instrumentos"><Button className="bg-amber text-dark hover:bg-[#f7c658]"><Plus size={15} /> Nueva evaluación</Button></a>
              <Link to="/colmena/company"><Button variant="ghost" className="border border-white/15 bg-white/10 text-white hover:bg-white/20"><Building2 size={15} /> {profileReady ? 'Datos de empresa' : 'Completar empresa'}</Button></Link>
            </div>
          </div>
          <div className="rounded-2xl border border-white/15 bg-white/10 p-4 backdrop-blur-xl">
            <div className="flex items-center justify-between"><div><p className="text-[10px] font-extrabold uppercase tracking-[.14em] text-white/50">Preparación documental</p><p className="mt-1 text-2xl font-black">{profile?.completeness_pct || 0}%</p></div><Target className="text-[#9ce8e4]" size={28} /></div>
            <div className="mt-3 h-2 overflow-hidden rounded-full bg-black/20"><div className="h-full rounded-full bg-gradient-to-r from-amber to-[#ffe49d]" style={{ width: `${profile?.completeness_pct || 0}%` }} /></div>
            <div className="mt-4 grid grid-cols-2 gap-2 text-xs"><div className="rounded-xl bg-black/15 p-3"><span className="block text-white/45">Población</span><strong className="mt-1 block">{profile?.worker_count || '—'} trabajadores</strong></div><div className="rounded-xl bg-black/15 p-3"><span className="block text-white/45">Privacidad</span><strong className="mt-1 block">Supresión n &lt; 5</strong></div></div>
          </div>
        </div>
      </section>

      <section className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
        <Metric icon={ClipboardCheck} label="Evaluaciones" value={campaigns.length} detail="Histórico de campañas de la empresa" />
        <Metric icon={Activity} label="En ejecución" value={active} detail="Con captura o análisis disponible" tone="green" />
        <Metric icon={Users} label="Marco poblacional" value={profile?.worker_count || '—'} detail="Denominador empresarial declarado" tone="teal" />
        <Metric icon={FileCheck2} label="Expediente" value="36 bloques" detail="Salida técnica, anexos y cuatro firmas" tone="amber" />
      </section>

      <section id="instrumentos">
        <div className="mb-4 flex flex-wrap items-end justify-between gap-3"><div><p className="text-[10px] font-extrabold uppercase tracking-[.14em] text-turquoise">Catálogo Colmena</p><h2 className="mt-1 text-xl font-black tracking-tight text-dark">¿Qué instrumento deseas aplicar?</h2><p className="mt-1 text-xs text-muted">El instrumento se congela cuando inicia la captura para asegurar trazabilidad.</p></div><span className="inline-flex items-center gap-2 rounded-full border border-border bg-white px-3 py-1.5 text-[10px] font-bold text-muted"><ShieldCheck size={13} className="text-turquoise" /> Núcleo protegido</span></div>
        <div className="grid gap-4 xl:grid-cols-2">{INSTRUMENTS.map((instrument) => <InstrumentCard key={instrument.code} instrument={instrument} profileReady={profileReady} />)}</div>
      </section>

      <section>
        <div className="mb-4 flex items-end justify-between gap-3"><div><p className="text-[10px] font-extrabold uppercase tracking-[.14em] text-amber">Próximamente</p><h2 className="mt-1 text-lg font-black text-dark">Biblioteca preventiva extensible</h2></div></div>
        <div className="grid gap-3 md:grid-cols-3">{FUTURE_INSTRUMENTS.map(([title, description, Icon]) => <div key={title} className="flex items-start gap-3 rounded-2xl border border-dashed border-border bg-white/55 p-4 opacity-75"><span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-slate-500"><Icon size={17} /></span><div className="min-w-0"><div className="flex items-center gap-2"><p className="text-sm font-bold text-dark">{title}</p><LockKeyhole size={12} className="text-muted" /></div><p className="mt-1 text-[11px] leading-4 text-muted">{description}</p></div></div>)}</div>
      </section>

      <section>
        <div className="mb-4 flex flex-wrap items-center justify-between gap-3"><div><p className="text-[10px] font-extrabold uppercase tracking-[.14em] text-turquoise">Operación</p><h2 className="mt-1 text-xl font-black text-dark">Campañas recientes</h2></div><Link to="/colmena/archive/projects" className="inline-flex items-center gap-1 text-xs font-bold text-turquoise">Ver histórico <ChevronRight size={14} /></Link></div>
        {campaigns.length ? <div className="grid gap-3 lg:grid-cols-2 2xl:grid-cols-3">{campaigns.slice(0, 6).map((project) => <CampaignCard key={project.id} project={project} />)}</div> : <Card><div className="flex flex-col items-center py-8 text-center"><CircleDashed size={34} className="text-amber" /><p className="mt-3 text-sm font-bold text-dark">Todavía no hay evaluaciones</p><p className="mt-1 max-w-md text-xs text-muted">Selecciona la versión corta o media para preparar la primera campaña de la empresa.</p></div></Card>}
      </section>

      <section className="grid gap-3 md:grid-cols-4">
        {[['1', 'Configura', 'Población, sedes y privacidad', Building2], ['2', 'Publica', 'Enlace, QR y códigos anónimos', CheckCircle2], ['3', 'Comprende', 'Telemetría y analítica prudente', BarChart3], ['4', 'Actúa', 'Plan, metas y expediente', FileCheck2]].map(([number, title, detail, Icon]) => <div key={number} className="flex gap-3 rounded-2xl border border-border bg-white p-4"><span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-dark text-white"><Icon size={16} /></span><div><p className="text-[9px] font-black uppercase tracking-wider text-amber">Paso {number}</p><p className="text-sm font-bold text-dark">{title}</p><p className="mt-0.5 text-[10px] text-muted">{detail}</p></div></div>)}
      </section>
    </div>
  );
}
