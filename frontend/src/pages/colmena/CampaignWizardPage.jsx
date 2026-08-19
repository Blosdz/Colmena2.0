import { useMemo, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import {
  ArrowLeft,
  ArrowRight,
  Building2,
  CalendarDays,
  Check,
  CheckCircle2,
  ClipboardCheck,
  Gauge,
  Info,
  Layers3,
  Link2,
  LockKeyhole,
  MapPin,
  Rocket,
  ShieldCheck,
  Sparkles,
  Target,
  Users,
} from 'lucide-react';

import { getCompanyProfile } from '../../api/company.js';
import { createDemoCampaign } from '../../api/demo.js';
import { createProject } from '../../api/projects.js';
import { useAuth } from '../../auth/AuthContext.jsx';
import { Button } from '../../components/ui/Button.jsx';
import { Card } from '../../components/ui/Card.jsx';
import { LoadingState } from '../../components/ui/LoadingState.jsx';

const STEPS = ['Instrumento', 'Alcance', 'Segmentación', 'Privacidad', 'Publicación'];

const VERSION_INFO = {
  SHORT: { name: 'CENSOPAS-COPSOQ corta', questions: 42, scored: 31, output: '6 dimensiones', duration: '8–12 min', icon: ClipboardCheck },
  MEDIUM: { name: 'CENSOPAS-COPSOQ media', questions: 112, scored: 69, output: '6 dimensiones ? 20 subdimensiones', duration: '18–25 min', icon: Layers3 },
};

const SEGMENTS = [
  ['AREA', 'Área o unidad', true],
  ['LOCATION', 'Sede', true],
  ['SHIFT', 'Turno', true],
  ['JOB_FAMILY', 'Familia ocupacional', true],
  ['CONTRACT', 'Tipo de contrato', false],
  ['AGE_RANGE', 'Rango de edad', false],
  ['SEX', 'Sexo', false],
  ['TENURE', 'Antigüedad', false],
];

function Stepper({ current }) {
  return (
    <div className="overflow-x-auto pb-1">
      <div className="flex min-w-[660px] items-center">
        {STEPS.map((label, index) => <div key={label} className="contents"><div className="flex items-center gap-2"><span className={`flex h-8 w-8 items-center justify-center rounded-full text-xs font-black ${index < current ? 'bg-turquoise text-white' : index === current ? 'bg-amber text-dark shadow-[0_0_0_5px_rgba(213,155,39,.12)]' : 'bg-slate-100 text-slate-400'}`}>{index < current ? <Check size={14} /> : index + 1}</span><span className={`text-xs font-bold ${index <= current ? 'text-dark' : 'text-muted'}`}>{label}</span></div>{index < STEPS.length - 1 ? <div className={`mx-3 h-px flex-1 ${index < current ? 'bg-turquoise' : 'bg-border'}`} /> : null}</div>)}
      </div>
    </div>
  );
}

function Toggle({ active, onClick, title, description }) {
  return <button type="button" onClick={onClick} className={`flex items-start gap-3 rounded-2xl border p-3 text-left transition ${active ? 'border-turquoise/45 bg-turquoise/8' : 'border-border bg-white hover:border-turquoise/25'}`}><span className={`mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-md border ${active ? 'border-turquoise bg-turquoise text-white' : 'border-slate-300'}`}>{active ? <Check size={13} /> : null}</span><span><span className="block text-xs font-bold text-dark">{title}</span><span className="mt-0.5 block text-[10px] leading-4 text-muted">{description}</span></span></button>;
}

export default function CampaignWizardPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [searchParams] = useSearchParams();
  const initialVersion = searchParams.get('instrument') === 'SHORT' ? 'SHORT' : 'MEDIUM';
  const [step, setStep] = useState(0);
  const [version, setVersion] = useState(initialVersion);
  const [form, setForm] = useState({
    name: 'Evaluación psicosocial 2026 ? Operación minera',
    expected_workers: 250,
    start_date: new Date().toISOString().slice(0, 10),
    end_date: new Date(Date.now() + 21 * 86400000).toISOString().slice(0, 10),
    segments: SEGMENTS.filter((item) => item[2]).map((item) => item[0]),
    min_publishable_n: 5,
    access_mode: 'ANONYMOUS_ONE_TIME_CODE',
    coverage_target: 85,
    coverage_critical: 65,
    completion_target: 90,
    risk_warning: 35,
    risk_critical: 50,
  });
  const profileQuery = useQuery({ queryKey: ['company-profile'], queryFn: getCompanyProfile });
  const profile = profileQuery.data;
  const info = VERSION_INFO[version];
  const VersionIcon = info.icon;

  const selectedLocations = useMemo(() => profile?.locations || [], [profile]);
  const update = (key, value) => setForm((current) => ({ ...current, [key]: value }));
  const toggleSegment = (code) => update('segments', form.segments.includes(code) ? form.segments.filter((item) => item !== code) : [...form.segments, code]);

  const createMutation = useMutation({
    mutationFn: async () => {
      const project = await createProject({
        ownerUserId: user.id,
        organizationId: profile.id,
        name: form.name,
        projectType: 'CENSO',
        description: `Campaña empresarial ${info.name} con captura anónima y expediente técnico.`,
        metadata: {
          product_mode: 'PSYCHOSOCIAL_COMPANY',
          methodology: 'CENSOPAS_COPSOQ',
          methodology_mode: 'COLMENA_EXPLORATORY_SYNTHETIC',
          instrument_version_kind: version,
          expected_worker_count: Number(form.expected_workers),
          start_date: form.start_date,
          end_date: form.end_date,
          enabled_segments: form.segments,
          company_snapshot: { id: profile.id, name: profile.name, legal_name: profile.legal_name, tax_id: profile.tax_id },
          locations_snapshot: selectedLocations,
          min_publishable_n: Number(form.min_publishable_n),
          anonymity_mode: form.access_mode,
          official_equivalence_enabled: false,
          campaign_status: 'OPEN',
          thresholds: {
            coverage_target: Number(form.coverage_target),
            coverage_critical: Number(form.coverage_critical),
            completion_target: Number(form.completion_target),
            risk_warning: Number(form.risk_warning),
            risk_critical: Number(form.risk_critical),
          },
        },
      });
      const campaign = await createDemoCampaign(project.id, { version_kind: version, synthetic_responses: 250, industry: 'MINERIA' });
      return { project, campaign };
    },
    onSuccess: ({ project }) => {
      queryClient.invalidateQueries({ queryKey: ['projects'] });
      queryClient.invalidateQueries({ queryKey: ['sidebar-projects'] });
      navigate(`/colmena/project/${project.id}`);
    },
  });

  if (profileQuery.isLoading) return <LoadingState label="Preparando la campaña…" />;
  if (!profile) return <div className="colmena-page"><Card><div className="py-8 text-center"><Building2 className="mx-auto text-amber" size={34} /><h1 className="mt-3 text-lg font-black text-dark">Primero completa los datos de la empresa</h1><p className="mt-1 text-sm text-muted">La campaña y el expediente necesitan razón social, RUC y población.</p><Link to="/colmena/company"><Button className="mt-4">Configurar empresa</Button></Link></div></Card></div>;

  const canContinue = step !== 1 || (form.name.trim() && Number(form.expected_workers) > 0 && form.end_date >= form.start_date);

  return (
    <div className="colmena-page pb-16">
      <div className="flex flex-wrap items-center justify-between gap-3"><Link to="/colmena" className="inline-flex items-center gap-2 text-xs font-bold text-muted hover:text-dark"><ArrowLeft size={14} /> Volver al catálogo</Link><span className="rounded-full border border-border bg-white px-3 py-1.5 text-[10px] font-extrabold uppercase tracking-wider text-muted">Borrador seguro</span></div>

      <section className="overflow-hidden rounded-[28px] border border-white/15 bg-gradient-to-br from-[#102f33] via-[#173e42] to-[#17635f] p-6 text-white shadow-[0_28px_70px_rgba(16,47,51,.22)] sm:p-8">
        <div className="grid gap-5 lg:grid-cols-[1.3fr_.7fr] lg:items-end"><div><span className="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/10 px-3 py-1.5 text-[10px] font-extrabold uppercase tracking-[.14em] text-[#9ce8e4]"><Sparkles size={13} /> Nueva evaluación</span><h1 className="mt-4 text-2xl font-black tracking-tight sm:text-3xl">Configura una campaña lista para publicar</h1><p className="mt-3 max-w-2xl text-sm leading-6 text-white/65">El instrumento, la privacidad y los umbrales se congelarán al iniciar la captura.</p></div><div className="rounded-2xl border border-white/15 bg-white/10 p-4"><p className="text-[10px] font-extrabold uppercase tracking-wider text-white/45">Empresa</p><p className="mt-1 text-sm font-bold">{profile.legal_name}</p><p className="mt-1 text-xs text-white/55">RUC {profile.tax_id} · {profile.worker_count} trabajadores</p></div></div>
      </section>

      <Card><Stepper current={step} /></Card>

      <div className="grid gap-4 xl:grid-cols-[minmax(0,1fr)_320px]">
        <Card>
          {step === 0 ? <div><div className="mb-5"><p className="text-[10px] font-extrabold uppercase tracking-[.14em] text-turquoise">Paso 1</p><h2 className="mt-1 text-xl font-black text-dark">Selecciona la profundidad del instrumento</h2><p className="mt-1 text-xs text-muted">La versión corta no publica subdimensiones. La media habilita veinte subdimensiones y resultados complementarios.</p></div><div className="grid gap-3 md:grid-cols-2">{Object.entries(VERSION_INFO).map(([code, item]) => { const Icon = item.icon; const selected = version === code; return <button key={code} type="button" onClick={() => setVersion(code)} className={`rounded-2xl border p-5 text-left transition ${selected ? 'border-turquoise bg-turquoise/7 shadow-[0_0_0_3px_rgba(24,167,161,.08)]' : 'border-border bg-white hover:border-turquoise/30'}`}><div className="flex items-start justify-between"><span className={`flex h-11 w-11 items-center justify-center rounded-xl ${selected ? 'bg-turquoise text-white' : 'bg-slate-100 text-slate-500'}`}><Icon size={20} /></span>{selected ? <CheckCircle2 className="text-turquoise" size={20} /> : null}</div><h3 className="mt-4 text-base font-black text-dark">{item.name}</h3><p className="mt-1 text-xs text-muted">{item.questions} preguntas · {item.scored} puntuables</p><p className="mt-3 rounded-xl bg-surfaceSoft px-3 py-2 text-[11px] font-semibold text-dark">{item.output}</p></button>; })}</div><div className="mt-4 flex items-start gap-3 rounded-2xl border border-amber/25 bg-amber/7 p-4"><Info className="mt-0.5 shrink-0 text-amber" size={18} /><p className="text-xs leading-5 text-muted">Con una población de <strong className="text-dark">{profile.worker_count} trabajadores</strong>, Colmena recomienda la versión media. La recomendación no bloquea la decisión profesional.</p></div></div> : null}

          {step === 1 ? <div><div className="mb-5"><p className="text-[10px] font-extrabold uppercase tracking-[.14em] text-turquoise">Paso 2</p><h2 className="mt-1 text-xl font-black text-dark">Define el alcance y la ventana de captura</h2></div><div className="grid gap-4 md:grid-cols-2"><label className="md:col-span-2"><span className="colmena-label">Nombre de la evaluación</span><input className="colmena-input mt-2 h-11" value={form.name} onChange={(event) => update('name', event.target.value)} /></label><label><span className="colmena-label">Población convocada</span><div className="relative mt-2"><Users className="absolute left-3 top-3 h-4 w-4 text-muted" /><input type="number" min="1" max="1000000" className="colmena-input h-11 pl-10" value={form.expected_workers} onChange={(event) => update('expected_workers', event.target.value)} /></div></label><label><span className="colmena-label">Regla de publicación</span><select className="colmena-input mt-2 h-11" value={form.min_publishable_n} onChange={(event) => update('min_publishable_n', event.target.value)}><option value="5">Ocultar grupos n &lt; 5</option><option value="7">Ocultar grupos n &lt; 7</option><option value="10">Ocultar grupos n &lt; 10</option></select></label><label><span className="colmena-label">Inicio</span><div className="relative mt-2"><CalendarDays className="absolute left-3 top-3 h-4 w-4 text-muted" /><input type="date" className="colmena-input h-11 pl-10" value={form.start_date} onChange={(event) => update('start_date', event.target.value)} /></div></label><label><span className="colmena-label">Cierre</span><div className="relative mt-2"><CalendarDays className="absolute left-3 top-3 h-4 w-4 text-muted" /><input type="date" className="colmena-input h-11 pl-10" value={form.end_date} onChange={(event) => update('end_date', event.target.value)} /></div></label></div></div> : null}

          {step === 2 ? <div><div className="mb-5"><p className="text-[10px] font-extrabold uppercase tracking-[.14em] text-turquoise">Paso 3</p><h2 className="mt-1 text-xl font-black text-dark">Activa las variables de segmentación</h2><p className="mt-1 text-xs text-muted">Solo se publicarán agregados que superen la regla mínima de privacidad.</p></div><div className="grid gap-3 md:grid-cols-2">{SEGMENTS.map(([code, title]) => <Toggle key={code} active={form.segments.includes(code)} onClick={() => toggleSegment(code)} title={title} description={code === 'AREA' || code === 'LOCATION' ? 'Catálogo organizacional controlado por la empresa.' : 'Categorías amplias para reducir riesgo de identificación.'} />)}</div><div className="mt-5"><p className="colmena-label mb-2">Sedes incluidas</p><div className="grid gap-2 md:grid-cols-3">{selectedLocations.map((location) => <div key={location.code} className="flex items-center gap-3 rounded-xl border border-border bg-surfaceSoft p-3"><MapPin size={15} className="text-turquoise" /><div><p className="text-xs font-bold text-dark">{location.name}</p><p className="text-[10px] text-muted">{location.worker_count} trabajadores</p></div></div>)}</div></div></div> : null}

          {step === 3 ? <div><div className="mb-5"><p className="text-[10px] font-extrabold uppercase tracking-[.14em] text-turquoise">Paso 4</p><h2 className="mt-1 text-xl font-black text-dark">Protege la participación y define los límites</h2></div><div className="grid gap-3 md:grid-cols-2"><Toggle active={form.access_mode === 'ANONYMOUS_ONE_TIME_CODE'} onClick={() => update('access_mode', 'ANONYMOUS_ONE_TIME_CODE')} title="Código anónimo de un solo uso" description="Evita duplicados sin asociar identidad con respuestas. Recomendado." /><Toggle active={form.access_mode === 'ANONYMOUS_LINK'} onClick={() => update('access_mode', 'ANONYMOUS_LINK')} title="Enlace anónimo general" description="Más simple, con menor control sobre duplicados." /></div><div className="mt-5 rounded-2xl border border-border bg-surfaceSoft/70 p-4"><div className="mb-4 flex items-center gap-2"><Gauge size={17} className="text-amber" /><p className="text-sm font-black text-dark">Metas y umbrales del tablero</p></div><div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">{[['coverage_target', 'Meta cobertura', '%'], ['coverage_critical', 'Cobertura crítica', '%'], ['completion_target', 'Meta completitud', '%'], ['risk_warning', 'Riesgo en vigilancia', '%'], ['risk_critical', 'Riesgo crítico', '%']].map(([key, label, suffix]) => <label key={key}><span className="text-[10px] font-bold text-muted">{label}</span><div className="relative mt-1"><input type="number" min="0" max="100" className="colmena-input h-10 pr-7 font-mono font-bold" value={form[key]} onChange={(event) => update(key, event.target.value)} /><span className="absolute right-3 top-2.5 text-xs text-muted">{suffix}</span></div></label>)}</div><div className="mt-4 flex flex-wrap gap-2 text-[10px] font-bold"><span className="rounded-full bg-emerald-50 px-3 py-1 text-emerald-700">Meta alcanzada</span><span className="rounded-full bg-amber/15 px-3 py-1 text-yellowDark">Vigilancia</span><span className="rounded-full bg-red-50 px-3 py-1 text-danger">Crítico</span></div></div><div className="mt-4 flex items-start gap-3 rounded-2xl bg-[#102f33] p-4 text-white"><LockKeyhole className="mt-0.5 shrink-0 text-[#9ce8e4]" size={18} /><p className="text-xs leading-5 text-white/65">No se almacenan nombre, DNI ni correo junto a las respuestas. Las tablas, gráficos, exportaciones y reportes aplican la misma supresión desde el backend.</p></div></div> : null}

          {step === 4 ? <div><div className="mb-5"><p className="text-[10px] font-extrabold uppercase tracking-[.14em] text-turquoise">Paso 5</p><h2 className="mt-1 text-xl font-black text-dark">Revisa y publica el escenario sintético</h2><p className="mt-1 text-xs text-muted">Se crearán 250 sesiones persistentes para demostrar telemetría, analítica y expediente.</p></div><div className="grid gap-3 md:grid-cols-2"><div className="rounded-2xl border border-border p-4"><p className="text-[10px] font-extrabold uppercase tracking-wider text-muted">Instrumento</p><p className="mt-2 text-sm font-black text-dark">{info.name}</p><p className="mt-1 text-xs text-muted">{info.questions} preguntas · {info.output}</p></div><div className="rounded-2xl border border-border p-4"><p className="text-[10px] font-extrabold uppercase tracking-wider text-muted">Aplicación</p><p className="mt-2 text-sm font-black text-dark">{form.expected_workers} convocados</p><p className="mt-1 text-xs text-muted">{form.start_date} — {form.end_date}</p></div><div className="rounded-2xl border border-border p-4"><p className="text-[10px] font-extrabold uppercase tracking-wider text-muted">Privacidad</p><p className="mt-2 text-sm font-black text-dark">n ≥ {form.min_publishable_n}</p><p className="mt-1 text-xs text-muted">{form.access_mode === 'ANONYMOUS_ONE_TIME_CODE' ? 'Códigos anónimos de un solo uso' : 'Enlace anónimo general'}</p></div><div className="rounded-2xl border border-border p-4"><p className="text-[10px] font-extrabold uppercase tracking-wider text-muted">Umbrales</p><div className="mt-2 flex gap-2 text-[10px] font-bold"><span className="rounded-full bg-emerald-50 px-2 py-1 text-emerald-700">Meta {form.coverage_target}%</span><span className="rounded-full bg-amber/15 px-2 py-1 text-yellowDark">Vigilar {form.risk_warning}%</span><span className="rounded-full bg-red-50 px-2 py-1 text-danger">Crítico {form.risk_critical}%</span></div></div></div><div className="mt-5 flex items-start gap-3 rounded-2xl border border-amber/25 bg-amber/7 p-4"><Info className="mt-0.5 shrink-0 text-amber" size={18} /><p className="text-xs leading-5 text-muted">La concordancia oficial permanece deshabilitada. El demo utiliza datos sintéticos y umbrales exploratorios claramente rotulados.</p></div></div> : null}

          <div className="mt-6 flex items-center justify-between border-t border-border pt-5"><Button type="button" variant="secondary" disabled={step === 0 || createMutation.isPending} onClick={() => setStep((current) => current - 1)}><ArrowLeft size={15} /> Atrás</Button>{step < STEPS.length - 1 ? <Button type="button" disabled={!canContinue} onClick={() => setStep((current) => current + 1)}>Continuar <ArrowRight size={15} /></Button> : <Button type="button" loading={createMutation.isPending} onClick={() => createMutation.mutate()} className="bg-gradient-to-r from-amber to-[#edbd50] text-dark"><Rocket size={16} /> Crear demo con 250 respuestas</Button>}</div>
          {createMutation.isError ? <p className="mt-4 rounded-xl bg-red-50 px-3 py-2 text-xs font-semibold text-danger">{createMutation.error?.message || 'No se pudo crear la campaña.'}</p> : null}
        </Card>

        <aside className="space-y-4 xl:sticky xl:top-20 xl:self-start">
          <Card><div className="flex items-start gap-3"><span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-[#16383d] text-white"><VersionIcon size={18} /></span><div><p className="text-[10px] font-extrabold uppercase tracking-wider text-muted">Selección actual</p><p className="mt-1 text-sm font-black text-dark">{info.name}</p></div></div><div className="mt-4 grid grid-cols-2 gap-2">{[[info.questions, 'preguntas'], [info.scored, 'puntuables'], [info.duration, 'duración'], [form.expected_workers, 'convocados']].map(([value, label]) => <div key={label} className="rounded-xl bg-surfaceSoft p-3"><p className="text-sm font-black text-dark">{value}</p><p className="text-[9px] uppercase tracking-wide text-muted">{label}</p></div>)}</div></Card>
          <Card><p className="text-xs font-black text-dark">Controles activos</p><div className="mt-3 space-y-2">{[[ShieldCheck, 'Anonimato colectivo'], [Target, `Supresión n < ${form.min_publishable_n}`], [Link2, 'Enlace y QR'], [Gauge, 'Metas y alertas'], [Rocket, 'Motor reproducible']].map(([Icon, label]) => <div key={label} className="flex items-center gap-2 rounded-xl border border-border/70 px-3 py-2 text-[11px] font-semibold text-muted"><Icon size={14} className="text-turquoise" />{label}</div>)}</div></Card>
        </aside>
      </div>
    </div>
  );
}
