import React, { useEffect, useState } from "react";
import axios from "axios";

export default function ProjectList() {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:8000/api/projects")
      .then(res => setProjects(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="bg-white p-4 rounded shadow">
      <h2 className="text-xl mb-2 font-semibold">Projects</h2>
      <ul>
        {projects.map(p => (
          <li key={p.id} className="border-b py-2">
            <strong>{p.jan}</strong> — {p.work_name}
          </li>
        ))}
      </ul>
    </div>
  );
}
