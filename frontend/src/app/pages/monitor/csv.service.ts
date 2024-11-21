import { Injectable } from "@angular/core";

@Injectable()
export class CsvService {
  constructor() {}

  /**
   * Genera un archivo CSV desde un JSON y lo descarga.
   * @param data Array de objetos JSON.
   * @param filename Nombre del archivo a descargar.
   */
  exportToCsv(data: any[], filename: string): void {
    if (!data || !data.length) {
      console.error("No hay datos para convertir a CSV.");
      return;
    }

    // Extraer encabezados (keys del primer objeto)
    const headers = Object.keys(data[0]);

    // Crear las filas CSV
    const rows = data.map((row) =>
      headers.map((header) => JSON.stringify(row[header] || "")).join(",")
    );

    // Unir encabezados y filas
    const csvContent = [headers.join(","), ...rows].join("\r\n");

    // Crear Blob
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });

    // Crear un enlace de descarga
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    link.setAttribute("download", `${filename}.csv`);
    link.style.visibility = "hidden";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
}
