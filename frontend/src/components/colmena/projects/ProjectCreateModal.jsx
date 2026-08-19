import { useEffect, useId, useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import {
  ArrowLeft,
  ArrowRight,
  ChevronRight,
  FileQuestion,
  FolderKanban,
  GraduationCap,
  Layers3,
  ListChecks,
  Lock,
  Plus,
  Search,
  SlidersHorizontal,
  Users,
} from 'lucide-react';

import { createProject } from '../../../api/projects.js';
import { cn } from '../../../utils/cn.js';
import { Button } from '../../ui/Button.jsx';
import FormField from '../../ui/FormField.jsx';
import { Modal } from '../../ui/Modal.jsx';

const PROJECT_TYPES = [
  { value: 'ACADEMIC', label: 'Académico', description: 'Tesis de grado, maestría o doctorado.', icon: GraduationCap },
  { value: 'CENSO', label: 'CensoPÁS', description: 'CENSOPAS-COPSOQ con instrumento, datos exógenos y baremo de referencia automáticos.', icon: Users },
  { value: 'RESEARCH', label: 'Investigación', description: 'Estudios científicos o institucionales.', icon: Search },
  { value: 'CUSTOM', label: 'Personalizado', description: 'Una estructura adaptada a tu caso.', icon: SlidersHorizontal },
];

const CENSOPAS_MODALITIES = [
  {
    value: 'MEDIA',
    label: 'CENSOPAS Media',
    description: '112 preguntas del núcleo oficial (6 dimensiones, 20 subdimensiones). Analítica estándar.',
  },
  {
    value: 'EXTENDIDA',
    label: 'CENSOPAS Extendida',
    description: 'Mismo núcleo de 112 preguntas, con analítica avanzada preactivada (segmentación, modelo multivariable, evolución temporal).',
  },
];

// Ambas modalidades usan el banco MEDIA (112 preguntas): "Extendida" no es una
// tercera versión de instrumento, solo activa más análisis por defecto — el
// propio banco de ítems prohíbe crear una tercera versión metodológica.
const MODALITY_VERSION_KIND = 'MEDIUM';

const STUDY_CONTEXT_FIELDS = [
  { key: 'companyName', label: 'Empresa / centro' },
  { key: 'population', label: 'Población' },
  { key: 'period', label: 'Periodo' },
  { key: 'areas', label: 'Áreas' },
  { key: 'positions', label: 'Puestos' },
  { key: 'shifts', label: 'Turnos' },
  { key: 'responsible', label: 'Responsable' },
];

const BASIC_TOOLS = [
  { key: 'official_results', label: 'Resultado CENSOPAS' },
  { key: 'descriptive', label: 'Perfil y distribuciones' },
  { key: 'data_quality', label: 'Calidad de respuestas' },
];

const STATISTICAL_TOOLS = [
  { key: 'confidence_intervals', label: 'Intervalos de confianza (IC 95%)' },
  { key: 'reliability', label: 'Confiabilidad (Alfa/Omega)' },
  { key: 'group_comparisons', label: 'Comparación entre grupos' },
  { key: 'correlations', label: 'Relaciones entre variables' },
];

const ADVANCED_TOOLS = [
  { key: 'clustering', label: 'Segmentación de perfiles' },
  { key: 'multivariable_model', label: 'Modelo multivariable' },
  { key: 'temporal_comparison', label: 'Evolución temporal' },
];

function defaultAnalysisTools(modality) {
  const advancedDefault = modality === 'EXTENDIDA';
  return {
    official_results: true,
    descriptive: true,
    data_quality: true,
    confidence_intervals: true,
    reliability: true,
    group_comparisons: true,
    correlations: true,
    clustering: advancedDefault,
    multivariable_model: advancedDefault,
    temporal_comparison: advancedDefault,
  };
}

const schema = z.object({
  name: z.string().trim().min(1, 'Ingresa un nombre').max(255, 'Usa 255 caracteres como máximo'),
  projectType: z.enum(['ACADEMIC', 'CENSO', 'RESEARCH', 'CUSTOM']),
  description: z.string().trim().max(1000, 'Usa 1000 caracteres como máximo').optional(),
});

const CENSO_STEPS = ['Modalidad', 'Estudio', 'Instrumento', 'Analítica'];

export default function ProjectCreateModal({ ownerUserId, onClose, onCreated }) {
  const formId = useId();
  const queryClient = useQueryClient();
  const {
    register,
    handleSubmit,
    setValue,
    watch,
    trigger,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(schema),
    defaultValues: { name: '', projectType: 'ACADEMIC', description: '' },
  });

  const selectedType = watch('projectType');
  const isCenso = selectedType === 'CENSO';

  const [step, setStep] = useState(1);
  const [modality, setModality] = useState('MEDIA');
  const [studyContext, setStudyContext] = useState({});
  const [analysisTools, setAnalysisTools] = useState(() => defaultAnalysisTools('MEDIA'));

  useEffect(() => {
    if (!isCenso) setStep(1);
  }, [isCenso]);

  const handleModalityChange = (value) => {
    setModality(value);
    setAnalysisTools(defaultAnalysisTools(value));
  };

  const toggleTool = (key) => {
    setAnalysisTools((current) => ({ ...current, [key]: !current[key] }));
  };

  const mutation = useMutation({
    mutationFn: (values) => {
      const metadata = isCenso
        ? {
            requested_version_kind: MODALITY_VERSION_KIND,
            censopas_modality: modality,
            study_context: studyContext,
            analysis_profile: Object.entries(analysisTools).some(
              ([key, enabled]) => enabled && ADVANCED_TOOLS.some((tool) => tool.key === key),
            )
              ? 'EXTENDED'
              : 'STANDARD',
            analysis_tools: analysisTools,
          }
        : undefined;
      return createProject({ ownerUserId, ...values, metadata });
    },
    onSuccess: (project) => {
      queryClient.invalidateQueries({ queryKey: ['projects'] });
      queryClient.invalidateQueries({ queryKey: ['archive-projects'] });
      queryClient.invalidateQueries({ queryKey: ['sidebar-projects'] });
      if (onCreated) onCreated(project);
      else onClose();
    },
  });

  const goNext = async () => {
    if (step === 2) {
      const valid = await trigger('name');
      if (!valid) return;
    }
    setStep((current) => Math.min(current + 1, CENSO_STEPS.length));
  };
  const goBack = () => setStep((current) => Math.max(current - 1, 1));

  const showWizardNav = isCenso && step < CENSO_STEPS.length;

  return (
    <Modal
      title="Crear proyecto"
      subtitle={
        isCenso
          ? `Paso ${step} de ${CENSO_STEPS.length}: ${CENSO_STEPS[step - 1]}`
          : 'Elige el contexto y Colmena preparará la estructura metodológica inicial.'
      }
      icon={FolderKanban}
      onClose={onClose}
      size="lg"
      preventClose={mutation.isPending}
      footer={
        <>
          <Button type="button" variant="secondary" size="lg" onClick={onClose} disabled={mutation.isPending}>
            Cancelar
          </Button>
          {isCenso && step > 1 ? (
            <Button type="button" variant="secondary" size="lg" onClick={goBack} disabled={mutation.isPending}>
              <ArrowLeft size={16} />
              Anterior
            </Button>
          ) : null}
          {showWizardNav ? (
            <Button type="button" size="lg" onClick={goNext} className="bg-gradient-to-r from-amber to-honey px-6 text-white shadow-soft hover:opacity-95">
              Siguiente
              <ArrowRight size={16} />
            </Button>
          ) : (
            <Button
              type="submit"
              form={formId}
              size="lg"
              loading={mutation.isPending}
              className="bg-gradient-to-r from-amber to-honey px-6 text-white shadow-soft hover:opacity-95"
            >
              <Plus size={16} />
              {isCenso ? 'Crear evaluación' : 'Crear proyecto'}
            </Button>
          )}
        </>
      }
    >
      <form id={formId} className="space-y-5" onSubmit={handleSubmit((values) => mutation.mutate(values))} noValidate>
        {!isCenso || step === 1 ? (
          <fieldset>
            <legend className="colmena-label mb-2">Tipo de proyecto</legend>
            <input type="hidden" {...register('projectType')} />
            <div className="grid gap-2 sm:grid-cols-2">
              {PROJECT_TYPES.map((type) => {
                const TypeIcon = type.icon;
                const selected = selectedType === type.value;
                return (
                  <button
                    key={type.value}
                    type="button"
                    aria-pressed={selected}
                    onClick={() => setValue('projectType', type.value, { shouldValidate: true })}
                    className={cn(
                      'flex items-start gap-3 rounded-xl border p-3 text-left transition focus:outline-none focus:ring-2 focus:ring-amber/30',
                      selected
                        ? 'border-amber bg-amber/10 shadow-sm'
                        : 'border-border bg-white hover:border-amber/40 hover:bg-yellowSoft/50',
                    )}
                  >
                    <span className={cn('flex h-9 w-9 shrink-0 items-center justify-center rounded-lg', selected ? 'bg-white text-amber' : 'bg-surfaceSoft text-muted')}>
                      <TypeIcon size={18} />
                    </span>
                    <span>
                      <span className="block text-sm font-semibold text-dark">{type.label}</span>
                      <span className="mt-0.5 block text-xs leading-4 text-muted">{type.description}</span>
                    </span>
                  </button>
                );
              })}
            </div>
          </fieldset>
        ) : null}

        {isCenso && step === 1 ? (
          <fieldset>
            <legend className="colmena-label mb-2">Modalidad CENSOPAS</legend>
            <div className="grid gap-2 sm:grid-cols-2">
              {CENSOPAS_MODALITIES.map((item) => {
                const selected = modality === item.value;
                return (
                  <button
                    key={item.value}
                    type="button"
                    aria-pressed={selected}
                    onClick={() => handleModalityChange(item.value)}
                    className={cn(
                      'rounded-xl border p-3 text-left transition focus:outline-none focus:ring-2 focus:ring-amber/30',
                      selected
                        ? 'border-amber bg-amber/10 shadow-sm'
                        : 'border-border bg-white hover:border-amber/40 hover:bg-yellowSoft/50',
                    )}
                  >
                    <span className="block text-sm font-semibold text-dark">{item.label}</span>
                    <span className="mt-0.5 block text-xs leading-4 text-muted">{item.description}</span>
                  </button>
                );
              })}
            </div>
          </fieldset>
        ) : null}

        {!isCenso || step === 2 ? (
          <>
            <FormField
              label="Nombre del proyecto"
              placeholder="Ej. Tesis de satisfacción académica"
              error={errors.name?.message}
              autoFocus
              autoComplete="off"
              {...register('name')}
            />
            <label className="flex flex-col gap-2">
              <span className="colmena-label">Descripción (opcional)</span>
              <textarea
                rows={3}
                placeholder="Resume el propósito y la población de estudio."
                className={cn(
                  'min-h-[88px] resize-y rounded-xl border bg-white px-3 py-2.5 text-sm text-dark outline-none transition placeholder:text-muted focus:border-amber focus:ring-2 focus:ring-amber/15',
                  errors.description ? 'border-danger' : 'border-border',
                )}
                {...register('description')}
              />
              {errors.description ? <span className="text-xs font-medium text-danger">{errors.description.message}</span> : null}
            </label>
          </>
        ) : null}

        {isCenso && step === 2 ? (
          <fieldset>
            <legend className="colmena-label mb-2">Datos del estudio (opcional)</legend>
            <div className="grid gap-3 sm:grid-cols-2">
              {STUDY_CONTEXT_FIELDS.map((field) => (
                <label key={field.key} className="flex flex-col gap-1.5">
                  <span className="text-xs font-medium text-muted">{field.label}</span>
                  <input
                    type="text"
                    value={studyContext[field.key] || ''}
                    onChange={(event) =>
                      setStudyContext((current) => ({ ...current, [field.key]: event.target.value }))
                    }
                    className="colmena-input h-10 px-3 text-sm text-dark placeholder:text-muted"
                  />
                </label>
              ))}
            </div>
          </fieldset>
        ) : null}

        {isCenso && step === 3 ? (
          <div className="space-y-3">
            <div className="flex items-start gap-3 rounded-2xl border border-border bg-white p-4">
              <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-surfaceSoft text-amber">
                <Lock size={16} />
              </span>
              <div>
                <p className="text-sm font-semibold text-dark">Preguntas núcleo bloqueadas</p>
                <p className="mt-0.5 text-xs leading-4 text-muted">
                  112 preguntas oficiales CENSOPAS-COPSOQ (6 dimensiones, 20 subdimensiones) — protegidas, no editables.
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3 rounded-2xl border border-border bg-white p-4">
              <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-surfaceSoft text-amber">
                <SlidersHorizontal size={16} />
              </span>
              <div>
                <p className="text-sm font-semibold text-dark">Catálogos adaptables</p>
                <p className="mt-0.5 text-xs leading-4 text-muted">Puesto y área se capturan como texto libre por proyecto.</p>
              </div>
            </div>
            {modality === 'EXTENDIDA' ? (
              <div className="rounded-2xl border border-amber/20 bg-yellowSoft/70 p-4">
                <p className="text-xs font-semibold uppercase tracking-[0.12em] text-yellowDark">Módulos extra</p>
                <p className="mt-1 text-xs leading-4 text-dark">Analítica avanzada habilitada en el siguiente paso.</p>
              </div>
            ) : null}
          </div>
        ) : null}

        {isCenso && step === 4 ? (
          <div className="space-y-4">
            <p className="text-xs leading-4 text-muted">
              Selecciona qué quieres analizar; Colmena elige el método estadístico apropiado.
            </p>
            <ToolGroup title="Básico" items={BASIC_TOOLS} tools={analysisTools} disabled />
            <ToolGroup title="Estadística" items={STATISTICAL_TOOLS} tools={analysisTools} onToggle={toggleTool} />
            <ToolGroup title="Analítica avanzada" items={ADVANCED_TOOLS} tools={analysisTools} onToggle={toggleTool} />
          </div>
        ) : null}

        {!isCenso ? (
          <div className="rounded-2xl border border-amber/20 bg-yellowSoft/70 p-4">
            <p className="mb-3 text-xs font-semibold uppercase tracking-[0.12em] text-yellowDark">Estructura del proyecto</p>
            <div className="flex flex-wrap items-center gap-2">
              {[
                [FolderKanban, 'Proyecto'],
                [Layers3, 'Variables'],
                [SlidersHorizontal, 'Dimensiones'],
                [FileQuestion, 'Preguntas'],
              ].map(([StepIcon, label], index) => (
                <div key={label} className="contents">
                  <span className="inline-flex items-center gap-1.5 rounded-xl border border-border bg-white px-2.5 py-2 text-xs font-semibold text-dark shadow-sm">
                    <StepIcon size={14} className="text-amber" />
                    {label}
                  </span>
                  {index < 3 ? <ChevronRight size={14} className="text-amber" /> : null}
                </div>
              ))}
            </div>
          </div>
        ) : null}

        {mutation.isError ? (
          <p role="alert" className="rounded-xl border border-danger/20 bg-danger/10 px-3 py-2.5 text-sm font-medium text-danger">
            {mutation.error?.message || 'No se pudo crear el proyecto.'}
          </p>
        ) : null}
      </form>
    </Modal>
  );
}

function ToolGroup({ title, items, tools, onToggle, disabled = false }) {
  return (
    <fieldset>
      <legend className="mb-2 flex items-center gap-1.5 text-xs font-semibold uppercase tracking-[0.1em] text-muted">
        <ListChecks size={13} />
        {title}
      </legend>
      <div className="grid gap-2 sm:grid-cols-2">
        {items.map((item) => (
          <label
            key={item.key}
            className={cn(
              'flex items-center gap-2 rounded-xl border border-border bg-white px-3 py-2.5 text-sm text-dark',
              disabled ? 'opacity-70' : 'cursor-pointer hover:border-amber/40',
            )}
          >
            <input
              type="checkbox"
              checked={Boolean(tools[item.key])}
              disabled={disabled}
              onChange={() => onToggle?.(item.key)}
              className="h-4 w-4 rounded border-border text-amber focus:ring-amber/30"
            />
            {item.label}
          </label>
        ))}
      </div>
    </fieldset>
  );
}
