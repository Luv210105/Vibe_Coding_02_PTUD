export default function DataTable({ columns, rows, emptyMessage, actions }) {
  return (
    <div className="overflow-hidden rounded-3xl border border-white/70 bg-white/90 shadow-panel">
      <div className="overflow-x-auto">
        <table className="min-w-full">
          <thead className="bg-slate-50">
            <tr>
              {columns.map((column) => (
                <th key={column.key} className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                  {column.label}
                </th>
              ))}
              {actions ? <th className="px-4 py-3 text-right text-xs font-semibold uppercase tracking-wide text-slate-500">Thao tác</th> : null}
            </tr>
          </thead>
          <tbody>
            {rows.length ? (
              rows.map((row) => (
                <tr key={row.id} className="border-t border-slate-100 align-top">
                  {columns.map((column) => (
                    <td key={`${row.id}-${column.key}`} className="table-cell">
                      {column.render ? column.render(row) : row[column.key] || "-"}
                    </td>
                  ))}
                  {actions ? <td className="table-cell text-right">{actions(row)}</td> : null}
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={columns.length + (actions ? 1 : 0)} className="px-4 py-10 text-center text-sm text-slate-500">
                  {emptyMessage}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}