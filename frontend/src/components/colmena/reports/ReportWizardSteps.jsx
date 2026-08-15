const STEPS = ['Estudio', 'Plantilla', 'Secciones', 'Privacidad', 'Generar'];

export default function ReportWizardSteps({ current }) {
  return (
    <div className="flex flex-wrap gap-2">
      {STEPS.map((label, index) => (
        <span key={label} className={`colmena-badge ${index === current ? 'bg-amber text-white' : 'bg-amber/10 text-yellowDark'}`}>
          {index + 1}. {label}
        </span>
      ))}
    </div>
  );
}
