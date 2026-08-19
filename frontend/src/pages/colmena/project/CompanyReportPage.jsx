import { useEffect, useMemo, useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { Link, useParams } from 'react-router-dom';
import {
  BadgeCheck,
  BarChart3,
  BookOpenCheck,
  Building2,
  Check,
  CheckCircle2,
  ClipboardCheck,
  Download,
  FileCheck2,
  FileText,
  Fingerprint,
  Gauge,
  LockKeyhole,
  PenLine,
  ShieldAlert,
  ShieldCheck,
  Sparkles,
  Stamp,
  Users,
} from 'lucide-react';

import { getIntelligenceSummary } from '../../../api/analytics.js';
import { getCompanyProfile } from '../../../api/company.js';
import { getCensopasReadiness } from '../../../api/instruments.js';
import { getProject } from '../../../api/projects.js';
import { createReport, createReportTemplate, getReport, getReportDownloadUrl } from '../../../api/reports.js';
import { getStudy, listStudies } from '../../../api/studies.js';
import { useAuth } from '../../../auth/AuthContext.jsx';
import { useActiveProject } from '../../../hooks/useActiveProject.js';
import StudySelector from '../../../components/colmena/StudySelector.jsx';
import { Button } from '../../../components/ui/Button.jsx';
import { Card } from '../../../components/ui/Card.jsx';
import { ErrorState } from '../../../components/ui/ErrorState.jsx';
import { LoadingState } from '../../../components/ui/LoadingState.jsx';
import { ProjectMissingState } from '../../../components/colmena/ProjectMissingState.jsx';

const REPORT_SECTIONS = ['portada', 'ficha_tecnica', 'participacion_privacidad', 'resultados_globales', 'dimensiones', 'subdimensiones', 'unidades_seguras', 'variables_descriptivas', 'hallazgos_premium', 'plan_accion', 'anexos', 'trazabilidad'];

const BLOCK_GROUPS = [
  { title: 'I. Control y contexto', icon: FileCheck2, blocks: ['Portada corporativa', 'Control documental', 'Registro de versiones', 'Firmas y conformidad', 'Resumen ejecutivo'] },
  { title: 'II. Empresa y alcance', icon: Users, blocks: ['Datos de la empresa', 'Antecedentes', 'Objetivos', 'Alcance organizacional', 'Población y cobertura'] },
  { title: 'III. Metodología', icon: BookOpenCheck, blocks: ['Instrumento aplicado', 'Versión y estructura', 'Procedimiento', 'Anonimato y confidencialidad', 'Criterios de validez'] },
  { title: 'IV. Calidad estadística', icon: Gauge, blocks: ['Completitud', 'Duración y patrones', 'Outliers y sensibilidad', 'Confiabilidad α/ω', 'Normalidad y decisión de pruebas'] },
  { title: 'V. Resultados', icon: BarChart3, blocks: ['Perfil sociolaboral', 'Seis dimensiones', 'Veinte subdimensiones', 'Sedes y áreas', 'Salud, bienestar y satisfacción'] },
  { title: 'VI. Analítica avanzada', icon: Sparkles, blocks: ['Intervalos de confianza', 'Comparaciones y efectos', 'Correlaciones ajustadas', 'Clústeres agregados', 'Limitaciones e incertidumbre'] },
  { title: 'VII. Acción preventiva', icon: ClipboardCheck, blocks: ['Priorización', 'Hipótesis de origen', 'Plan de intervención', 'Balanced Scorecard', 'Cronograma y seguimiento'] },
  { title: 'VIII. Anexos', icon: Fingerprint, blocks: ['Instrumento', 'Tablas técnicas', 'Trazabilidad y hashes', 'Evidencias de campaña', 'Glosario metodológico', 'Declaración de limitaciones'] },
];

function ReadinessMetric({ icon: Icon, label, value, detail, ok = true }) {
  return <div className="rounded-2xl border border-white/70 bg-white/84 p-4 shadow-[0_14px_36px_rgba(22,56,61,.07)] backdrop-blur-xl"><div className="flex items-start justify-between"><span className={`flex h-9 w-9 items-center justify-center rounded-xl ${ok ? 'bg-emerald-50 text-emerald-700' : 'bg-amber/15 text-yellowDark'}`}><Icon size={17} /></span><span className={`rounded-full px-2 py-1 text-[8px] font-black uppercase ${ok ? 'bg-emerald-50 text-emerald-700' : 'bg-amber/15 text-yellowDark'}`}>{ok ? 'Listo' : 'Pendiente'}</span></div><p className="mt-4 text-[9px] font-black uppercase tracking-wider text-muted">{label}</p><p className="mt-1 text-xl font-black text-dark">{value}</p><p className="mt-1 text-[10px] leading-4 text-muted">{detail}</p></div>;
}

export default function CompanyReportPage() {
  const { projectId } = useParams();
  const { user } = useAuth();
  useActiveProject(projectId);
  const [studyId, setStudyId] = useState(null);
  const [format, setFormat] = useState('DOCX');
  const [report, setReport] = useState(null);

  const projectQuery = useQuery({ queryKey: ['project', projectId], queryFn: () => getProject(projectId) });
  const profileQuery = useQuery({ queryKey: ['company-profile'], queryFn: getCompanyProfile });
  const studiesQuery = useQuery({ queryKey: ['studies', projectId, 'report-company'], queryFn: () => listStudies(projectId, { page: 1, pageSize: 100 }) });
  useEffect(() => { if (!studyId && studiesQuery.data?.items?.length) setStudyId(studiesQuery.data.items[0].id); }, [studyId, studiesQuery.data]);
  const studyQuery = useQuery({ queryKey: ['study', studyId], queryFn: () => getStudy(studyId), enabled: Boolean(studyId) });
  const readinessQuery = useQuery({ queryKey: ['censopas-readiness', studyQuery.data?.instrument_version_id], queryFn: () => getCensopasReadiness(studyQuery.data.instrument_version_id), enabled: Boolean(studyQuery.data?.instrument_version_id) });
  const intelligenceQuery = useQuery({ queryKey: ['intelligence-summary', studyId], queryFn: () => getIntelligenceSummary(studyId), enabled: Boolean(studyId), staleTime: 60000 });

  const generation = useMutation({
    mutationFn: async () => {
      const template = await createReportTemplate({
        name: 'Expediente técnico empresarial Colmena',
        report_type: 'CENSOPAS_COPSOQ',
        instrument_version_id: studyQuery.data?.instrument_version_id,
        template_config: { methodology: 'CENSOPAS_COPSOQ', structure_version: 'SUNAFIL-DEMO-36', signatories: profileQuery.data?.signatories || [] },
      });
      return createReport(studyId, { report_template_id: template.id, output_format: format, requested_by_user_id: user.id, report_mode: 'PROVISIONAL', sections: REPORT_SECTIONS });
    },
    onSuccess: setReport,
  });
  const statusQuery = useQuery({ queryKey: ['report', report?.id], queryFn: () => getReport(report.id), enabled: Boolean(report?.id), refetchInterval: (query) => query.state.data && ['COMPLETED', 'FAILED'].includes(query.state.data.status) ? false : 1500 });

  const profile = profileQuery.data;
  const readiness = readinessQuery.data;
  const intelligence = intelligenceQuery.data;
  const signatoriesReady = (profile?.signatories || []).filter((item) => item.full_name).length;
  const totalBlocks = useMemo(() => BLOCK_GROUPS.reduce((total, group) => total + group.blocks.length, 0), []);
  const methodologicalReady = Boolean(readiness?.ready_for_scoring);
  const canGenerate = Boolean(studyId && methodologicalReady && profile?.tax_id);

  if (projectQuery.isLoading || profileQuery.isLoading) return <LoadingState label="Preparando el expediente…" />;
  if (projectQuery.isError || profileQuery.isError) return <ErrorState title="No pudimos preparar el expediente" message={projectQuery.error?.message || profileQuery.error?.message} />;
  if (!projectQuery.data) return <ProjectMissingState />;

  return (
    <div className="colmena-page pb-16">
      <section className="relative overflow-hidden rounded-[30px] border border-white/15 bg-gradient-to-br from-[#0d2d31] via-[#153e42] to-[#3b3521] p-6 text-white shadow-[0_30px_80px_rgba(16,47,51,.24)] sm:p-8">
        <div className="absolute -right-20 -top-28 h-72 w-72 rounded-full bg-amber/18 blur-3xl" />
        <div className="relative grid gap-6 xl:grid-cols-[1.3fr_.7fr] xl:items-end"><div><span className="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/10 px-3 py-1.5 text-[10px] font-black uppercase tracking-[.15em] text-[#ffe29b]"><Stamp size={14} /> Expediente técnico</span><h1 className="mt-4 text-2xl font-black tracking-tight sm:text-3xl">Informe CENSOPAS listo para revisión profesional</h1><p className="mt-3 max-w-3xl text-sm leading-6 text-white/65">Estructura integral con control documental, metodología, calidad, estadística avanzada, intervención, anexos y cuatro espacios de firma.</p><div className="mt-5 flex flex-wrap gap-2"><span className="rounded-full bg-amber px-3 py-1 text-[10px] font-black text-dark">BORRADOR TÉCNICO</span><span className="rounded-full border border-white/15 bg-white/8 px-3 py-1 text-[10px] font-bold text-white/70">{totalBlocks} bloques</span><span className="rounded-full border border-white/15 bg-white/8 px-3 py-1 text-[10px] font-bold text-white/70">4 firmas</span></div></div><div className="rounded-2xl border border-white/15 bg-white/10 p-4 backdrop-blur-xl"><p className="text-[9px] font-black uppercase tracking-wider text-white/45">Aplicación documental</p><div className="mt-3 [&_label]:text-white/65 [&_select]:border-white/15 [&_select]:bg-white/10 [&_select]:text-white"><StudySelector projectId={projectId} studyId={studyId} onStudyChange={setStudyId} /></div><p className="mt-4 text-[10px] leading-4 text-white/55">La versión final debe ser revisada y firmada. Colmena no convierte una salida provisional en oficial sin concordancia y baremo habilitados.</p></div></div>
      </section>

      <section className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
        <ReadinessMetric icon={Building2} label="Empresa" value={profile?.completeness_pct ? `${profile.completeness_pct}%` : '—'} detail={`${profile?.legal_name || 'Sin razón social'} · RUC ${profile?.tax_id || 'pendiente'}`} ok={Boolean(profile?.tax_id)} />
        <ReadinessMetric icon={ShieldCheck} label="Metodología" value={methodologicalReady ? 'Validada' : 'Revisar'} detail={`${readiness?.actual?.questions || 0}/${readiness?.expected?.questions || '—'} preguntas · versión ${readiness?.version_kind || '—'}`} ok={methodologicalReady} />
        <ReadinessMetric icon={Gauge} label="Analítica" value={intelligence ? `${intelligence.dimensions.length} dimensiones` : 'Procesando'} detail={intelligence ? `${intelligence.correlations.filter((item) => item.significant).length} asociaciones ajustadas · ${intelligence.quality.outlier_sessions} atípicos` : 'Evaluando confiabilidad y sensibilidad'} ok={Boolean(intelligence)} />
        <ReadinessMetric icon={PenLine} label="Firmantes" value={`${signatoriesReady}/4`} detail="Profesional, empresa, seguridad y psicología" ok={signatoriesReady === 4} />
      </section>

      <section className="grid gap-4 xl:grid-cols-[1.2fr_.8fr]">
        <Card>
          <div className="mb-5 flex flex-wrap items-start justify-between gap-3"><div><p className="text-[9px] font-black uppercase tracking-[.15em] text-turquoise">Índice maestro</p><h2 className="mt-1 text-lg font-black text-dark">Estructura completa del expediente</h2><p className="mt-1 text-xs text-muted">Cada bloque conserva denominadores, privacidad, versión y fuente de cálculo.</p></div><span className="rounded-full bg-emerald-50 px-3 py-1 text-[9px] font-black text-emerald-700">{totalBlocks}/{totalBlocks} incluidos</span></div>
          <div className="grid gap-3 md:grid-cols-2">{BLOCK_GROUPS.map((group) => { const Icon = group.icon; return <div key={group.title} className="rounded-2xl border border-border bg-white p-4"><div className="flex items-center gap-2"><span className="flex h-8 w-8 items-center justify-center rounded-xl bg-[#16383d] text-white"><Icon size={15} /></span><p className="text-xs font-black text-dark">{group.title}</p></div><div className="mt-3 space-y-1.5">{group.blocks.map((block) => <div key={block} className="flex items-center gap-2 text-[10px] text-muted"><span className="flex h-4 w-4 items-center justify-center rounded-full bg-emerald-50 text-emerald-700"><Check size={9} strokeWidth={3} /></span>{block}</div>)}</div></div>; })}</div>
        </Card>

        <div className="space-y-4">
          <Card>
            <div className="flex items-start justify-between"><div><p className="text-[9px] font-black uppercase tracking-[.14em] text-amber">Control metodológico</p><h2 className="mt-1 text-base font-black text-dark">Estado de emisión</h2></div><LockKeyhole size={20} className="text-amber" /></div>
            <div className="mt-4 space-y-2">{[[Boolean(profile?.tax_id), 'Identidad empresarial'], [methodologicalReady, 'Estructura y scoring'], [Boolean(intelligence), 'Analítica avanzada'], [true, 'Privacidad n ≥ 5'], [readiness?.ready_for_official_reporting, 'Equivalencia oficial']].map(([ok, label]) => <div key={label} className="flex items-center justify-between rounded-xl border border-border px-3 py-2.5"><span className="text-[11px] font-semibold text-dark">{label}</span>{ok ? <CheckCircle2 size={15} className="text-emerald-600" /> : <ShieldAlert size={15} className="text-amber" />}</div>)}</div>
            {!readiness?.ready_for_official_reporting ? <div className="mt-4 rounded-xl border border-amber/25 bg-amber/7 p-3"><p className="text-[10px] leading-4 text-muted">La versión oficial permanece bloqueada. El archivo se rotula como provisional y conserva la limitación en portada y trazabilidad.</p></div> : null}
          </Card>

          <Card>
            <div className="flex items-start justify-between"><div><p className="text-[9px] font-black uppercase tracking-[.14em] text-turquoise">Firmas</p><h2 className="mt-1 text-base font-black text-dark">Conformidad profesional</h2></div><BadgeCheck size={20} className="text-turquoise" /></div>
            <div className="mt-4 space-y-2">{(profile?.signatories || []).map((item) => <div key={item.role} className="rounded-xl border border-border p-3"><div className="flex items-center justify-between"><p className="text-[10px] font-black text-dark">{item.role}</p><span className={`h-2 w-2 rounded-full ${item.full_name ? 'bg-emerald-500' : 'bg-amber'}`} /></div><p className="mt-1 text-[10px] text-muted">{item.full_name || 'Nombre pendiente'}{item.professional_id ? ` · ${item.professional_id}` : ''}</p></div>)}</div>
            <Link to="/colmena/company" className="mt-3 inline-flex items-center gap-1 text-[10px] font-bold text-turquoise">Editar firmantes →</Link>
          </Card>
        </div>
      </section>

      <Card>
        <div className="grid gap-5 xl:grid-cols-[1fr_auto] xl:items-center"><div><div className="flex items-center gap-3"><span className="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br from-amber to-[#efbf58] text-dark shadow-lg"><FileText size={20} /></span><div><p className="text-[9px] font-black uppercase tracking-[.14em] text-amber">Generación</p><h2 className="text-lg font-black text-dark">Crear expediente provisional</h2></div></div><p className="mt-3 max-w-3xl text-xs leading-5 text-muted">El documento incorpora resultados agregados, gráficos, análisis complementario persistido, plan preventivo y anexo de trazabilidad. No contiene respuestas individuales.</p></div><div className="flex flex-wrap items-center gap-2"><select className="colmena-input h-10 w-40" value={format} onChange={(event) => setFormat(event.target.value)}><option value="DOCX">Word editable</option><option value="PDF">PDF</option></select><Button loading={generation.isPending} disabled={!canGenerate} onClick={() => generation.mutate()} className="bg-gradient-to-r from-amber to-[#efbf58] text-dark"><FileCheck2 size={15} /> Generar expediente</Button></div></div>
        {!canGenerate ? <p className="mt-4 rounded-xl bg-amber/7 px-3 py-2 text-[10px] font-semibold text-yellowDark">Completa la empresa y valida la estructura del estudio antes de generar.</p> : null}
        {generation.isError ? <p className="mt-4 rounded-xl bg-red-50 px-3 py-2 text-[10px] font-semibold text-danger">{generation.error?.message || 'No se pudo generar el expediente.'}</p> : null}
        {report ? <div className="mt-5 flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-turquoise/20 bg-turquoise/5 p-4"><div className="flex items-center gap-3">{statusQuery.data?.status === 'COMPLETED' ? <CheckCircle2 className="text-emerald-600" /> : <FileText className="text-turquoise" />}<div><p className="text-xs font-black text-dark">{statusQuery.data?.status === 'COMPLETED' ? 'Expediente generado' : 'Construyendo documento…'}</p><p className="mt-0.5 text-[10px] text-muted">ID {report.public_id || report.id} · formato {format}</p></div></div>{statusQuery.data?.status === 'COMPLETED' ? <a href={getReportDownloadUrl(report.id)} target="_blank" rel="noreferrer"><Button size="sm"><Download size={14} /> Descargar {format}</Button></a> : <LoadingState label="Generando…" />}</div> : null}
      </Card>

      <Card className="border-amber/25 bg-amber/5"><div className="flex items-start gap-3"><ShieldAlert className="mt-0.5 shrink-0 text-amber" size={19} /><div><p className="text-xs font-black text-dark">Revisión obligatoria</p><p className="mt-1 text-[10px] leading-4 text-muted">La narrativa automática describe resultados colectivos y limitaciones; no diagnostica personas ni establece causalidad. El psicólogo, el ingeniero de seguridad, el profesional responsable y la empresa deben revisar y firmar la versión final.</p></div></div></Card>
    </div>
  );
}
