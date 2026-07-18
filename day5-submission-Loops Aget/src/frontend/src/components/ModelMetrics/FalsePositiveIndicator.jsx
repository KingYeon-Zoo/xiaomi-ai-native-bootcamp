import { AlertTriangle } from "lucide-react";
import { useTranslation } from "react-i18next";

export default function FalsePositiveIndicator({ data }) {
  const { t } = useTranslation();

  const count = data?.count || 0;
  const isWarning = count > 0;

  return (
    <div
      className={`rounded-xl shadow-sm border p-5 ${
        isWarning
          ? "bg-amber-50/80 border-amber-200"
          : "bg-white/80 border-gray-200/60"
      }`}
    >
      <div className="flex items-center gap-2 mb-2">
        <AlertTriangle
          className={`w-4 h-4 ${isWarning ? "text-amber-600" : "text-gray-400"}`}
        />
        <h3 className="text-sm font-semibold text-gray-900">
          {t("metrics.potentialFalsePositives", "Potential False Positives")}
        </h3>
      </div>
      <p
        className={`text-3xl font-bold ${
          isWarning ? "text-amber-700" : "text-gray-900"
        }`}
      >
        {count}
      </p>
      <p className="text-[11px] text-gray-500 mt-1">
        {t("metrics.falsePositiveDesc", "ML predicted SAFE with high confidence, but rule engine blocked")}
      </p>
      {isWarning && (
        <div className="mt-3 px-2.5 py-1.5 rounded-lg bg-amber-100 text-amber-800 text-[11px] font-medium">
          ⚠ {t("metrics.falsePositiveWarning", "Review these posts — rules may be over-blocking")}
        </div>
      )}
    </div>
  );
}

