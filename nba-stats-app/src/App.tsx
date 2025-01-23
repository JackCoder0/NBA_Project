import React, { useState } from "react";
import axios from "axios";

function App() {
  const [playerName, setPlayerName] = useState("");
  const [playerStats, setPlayerStats] = useState(null);
  const [error, setError] = useState("");

  const fetchPlayerStats = async () => {
    try {
      setError("");
      setPlayerStats(null);
      const response = await axios.get("http://127.0.0.1:5000/player", {
        params: { name: playerName },
      });
      setPlayerStats(response.data);
    } catch (err) {
      setError(
        err.response?.data?.error || "Ocorreu um erro ao buscar o jogador"
      );
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>NBA Player Stats</h1>
      <input
        type="text"
        placeholder="Digite o nome do jogador"
        value={playerName}
        onChange={(e) => setPlayerName(e.target.value)}
        style={{ padding: "10px", width: "300px" }}
      />
      <button onClick={fetchPlayerStats} style={{ padding: "10px", marginLeft: "10px" }}>
        Buscar
      </button>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {playerStats && (
        <div style={{ marginTop: "20px" }}>
          <h2>Estatísticas de {playerStats.player_name}</h2>
          <table border="1" cellPadding="10">
            <thead>
              <tr>
                {Object.keys(playerStats.stats[0]).map((key) => (
                  <th key={key}>{key}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {playerStats.stats.map((row, index) => (
                <tr key={index}>
                  {Object.values(row).map((value, i) => (
                    <td key={i}>{value}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;
