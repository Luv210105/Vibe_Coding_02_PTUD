import { useEffect, useState } from "react";

export default function FormModal({ open, title, fields, initialValues, onClose, onSubmit, submitLabel = "Lưu" }) {
  const [formData, setFormData] = useState({});

  useEffect(() => {
    setFormData(initialValues || {});
  }, [initialValues]);

  if (!open) return null;

  const handleChange = (name, value) => {
    setFormData((current) => ({ ...current, [name]: value }));
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/45 p-4">
      <div className="w-full max-w-2xl rounded-3xl bg-white p-6 shadow-2xl">
        <div className="mb-6 flex items-center justify-between">
          <h3 className="text-xl font-bold text-slate-800">{title}</h3>
          <button className="secondary-button" onClick={onClose}>
            Đóng
          </button>
        </div>
        <form
          className="grid gap-4 md:grid-cols-2"
          onSubmit={(event) => {
            event.preventDefault();
            onSubmit(formData);
          }}
        >
          {fields.map((field) => (
            <label key={field.name} className={field.fullWidth ? "md:col-span-2" : ""}>
              <span className="field-label">{field.label}</span>
              {field.type === "select" ? (
                <select
                  className="field-input"
                  value={formData[field.name] ?? ""}
                  onChange={(event) => handleChange(field.name, event.target.value)}
                  required={field.required}
                >
                  <option value="">Chọn</option>
                  {field.options.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              ) : field.type === "textarea" ? (
                <textarea
                  className="field-input min-h-28"
                  value={formData[field.name] ?? ""}
                  onChange={(event) => handleChange(field.name, event.target.value)}
                  required={field.required}
                />
              ) : (
                <input
                  className="field-input"
                  type={field.type || "text"}
                  value={formData[field.name] ?? ""}
                  onChange={(event) => handleChange(field.name, event.target.value)}
                  required={field.required}
                  min={field.min}
                />
              )}
            </label>
          ))}
          <div className="md:col-span-2 flex justify-end gap-3 pt-2">
            <button type="button" className="secondary-button" onClick={onClose}>
              Hủy
            </button>
            <button type="submit" className="primary-button">
              {submitLabel}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}