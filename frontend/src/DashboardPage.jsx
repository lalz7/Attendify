import React from "react";

function DashboardPage() {
  // Data dummy absensi
  const absensi = [
    { tanggal: "2025-05-15", jamMasuk: "08:00", jamPulang: "17:00", status: "Hadir" },
    { tanggal: "2025-05-14", jamMasuk: "08:10", jamPulang: "17:05", status: "Hadir" },
    { tanggal: "2025-05-13", jamMasuk: "-", jamPulang: "-", status: "Izin" },
  ];

  return (
    <div className="container py-5">
      <div className="bg-white rounded-4 shadow-lg p-4 mb-4">
        <h2 className="mb-3 text-primary">Dashboard Absensi Karyawan</h2>
        <p className="mb-1">Selamat datang, <b>Karyawan</b>!</p>
        <button className="btn btn-outline-danger btn-sm float-end">Logout</button>
      </div>
      <div className="bg-white rounded-4 shadow-lg p-4">
        <h4 className="mb-3">Riwayat Absensi</h4>
        <div className="table-responsive">
          <table className="table table-bordered align-middle">
            <thead className="table-light">
              <tr>
                <th>Tanggal</th>
                <th>Jam Masuk</th>
                <th>Jam Pulang</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {absensi.map((row, idx) => (
                <tr key={idx}>
                  <td>{row.tanggal}</td>
                  <td>{row.jamMasuk}</td>
                  <td>{row.jamPulang}</td>
                  <td>
                    <span className={
                      row.status === "Hadir"
                        ? "badge bg-success"
                        : row.status === "Izin"
                        ? "badge bg-warning text-dark"
                        : "badge bg-secondary"
                    }>
                      {row.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default DashboardPage;