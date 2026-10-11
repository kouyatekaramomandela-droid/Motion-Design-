# Voix off Gemini TTS — en attente de la clé

La clé est lue dans la variable d'environnement `GEMINI_API_KEY` (à ajouter dans les réglages de l'environnement,
jamais dans un fichier du projet). Ensuite, depuis la racine du projet :

```bash
node /root/.claude/skills/media-use/audio/scripts/audio.mjs --request ./audio/vo_request.json --hyperframes . --out ./audio/vo_engine.json --only tts
python3 tools/build_vo.py
<venv>/bin/python tools/synth_score.py   # le ducking suit alors la vraie voix
tools/mix_audio.sh
python3 tools/build.py
```

- `vo_request.json` : 26 répliques, voix Gemini « Puck », modèle gemini-3.8-flash-tts, direction de jeu (accent de Conakry).
- `vo_plan.json` : l'instant de chaque réplique dans le film et sa durée maximale.
