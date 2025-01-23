from flask import Flask, jsonify, request
from flask_cors import CORS
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.live.nba.endpoints import scoreboard

app = Flask(__name__)
CORS(app)  # Permite conexões do frontend (React)

# Rota para buscar jogadores pelo nome
@app.route('/player', methods=['GET'])
def get_player_stats():
    player_name = request.args.get('name')
    if not player_name:
        return jsonify({"error": "Nome do jogador não foi fornecido"}), 400

    # Busca o ID do jogador
    player_list = players.get_players()
    player = next((p for p in player_list if p['full_name'].lower() == player_name.lower()), None)

    if not player:
        return jsonify({"error": f"Jogador '{player_name}' não encontrado"}), 404

    player_info = commonplayerinfo.CommonPlayerInfo(player_id=player['id'])
    bio_data = player_info.get_data_frames()[0]  # DataFrame com informações biográficas
    bio_json = bio_data.to_dict(orient='records')[0]

    # Obtém as estatísticas de carreira
    career_stats = playercareerstats.PlayerCareerStats(player_id=player['id'])
    stats_df = career_stats.get_data_frames()[0]

    # Converte o DataFrame para um formato JSON
    stats_json = stats_df.to_dict(orient='records')

    return jsonify({
        "player_name": player['full_name'],
        "bio": bio_json,
        "stats": stats_json
    })

@app.route('/games', methods=['GET'])
def get_games():
    try:
        # Obtém os jogos do dia
        games = scoreboard.ScoreBoard()

        # Converte os dados para JSON e dicionário
        games_json = games.get_json()  # Dados brutos em JSON
        games_dict = games.get_dict()  # Dados estruturados em dicionário

        return jsonify({
            "games": games_dict  # Retorna o dicionário estruturado
        })

    except Exception as e:
        return jsonify({"error": f"Erro ao buscar os jogos: {str(e)}"}), 500

# Roda o servidor
if __name__ == '__main__':
    app.run(debug=True)
