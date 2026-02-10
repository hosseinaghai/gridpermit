import { X } from "lucide-react";
import { useT } from "../i18n/translations";
import { useWorkflowStore } from "../store/workflowStore";

interface Props {
  isOpen: boolean;
  onClose: () => void;
}

export default function Impressum({ isOpen, onClose }: Props) {
  const t = useT();
  const language = useWorkflowStore((s) => s.language);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-end justify-center bg-black/40 sm:items-center">
      <div className="relative w-full max-w-lg rounded-t-xl bg-white p-5 shadow-2xl sm:mx-4 sm:rounded-xl sm:p-8">
        <button
          onClick={onClose}
          className="absolute right-3 top-3 rounded-lg p-2 text-gray-400 transition hover:bg-gray-100 hover:text-gray-600 sm:right-4 sm:top-4 sm:p-1"
        >
          <X className="h-5 w-5" />
        </button>

        <h2 className="text-xl font-bold text-gray-900">Impressum</h2>

        {language === "en" && (
          <p className="mt-2 rounded-md bg-blue-50 px-3 py-2 text-xs text-blue-700">
            {t("impressum.germanLawNote")}
          </p>
        )}

        <div className="mt-6 space-y-4 text-sm text-gray-700">
          <div>
            <h3 className="font-semibold text-gray-900">Verantwortlich</h3>
            <p className="mt-1">Hossein Aghai</p>
          </div>

          <div>
            <h3 className="font-semibold text-gray-900">Urheberrecht</h3>
            <p className="mt-1">
              Alle Inhalte, Texte, Grafiken, Software und sonstigen Bestandteile
              dieser Anwendung sind urheberrechtlich geschützt. Alle Rechte sind
              Hossein Aghai vorbehalten. Jegliche Vervielfältigung, Verbreitung,
              Bearbeitung oder sonstige Nutzung bedarf der vorherigen
              schriftlichen Zustimmung von Hossein Aghai.
            </p>
          </div>

          <div>
            <h3 className="font-semibold text-gray-900">Haftungsausschluss</h3>
            <p className="mt-1">
              Die in dieser Anwendung bereitgestellten Informationen und
              generierten Texte dienen ausschließlich der Unterstützung bei der
              Projektarbeit und stellen keine Rechtsberatung dar. Für die
              Richtigkeit, Vollständigkeit und Aktualität der Inhalte wird keine
              Gewähr übernommen.
            </p>
          </div>
        </div>

        <div className="mt-8 border-t border-gray-100 pt-4">
          <p className="text-xs text-gray-400">
            &copy; {new Date().getFullYear()} Hossein Aghai. {t("layout.allRightsReserved")}
          </p>
        </div>
      </div>
    </div>
  );
}
