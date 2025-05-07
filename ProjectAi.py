import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

from transformers import pipeline

# Load pre-trained emotion detection model
emotion_analyzer = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True
)

# Emoji map for emotions
emoji_map = {
    "joy": "😄",
    "anger": "😡",
    "sadness": "😢",
    "fear": "😨",
    "love": "❤️",
    "surprise": "😲",
    "neutral": "😐"
}

print("🎉 Welcome to AI Sentiment + Emotion Analyzer 🎉")
print("Type your sentence below (type 'bye' to exit):")

# Open chat history file
with open("chat_history.txt", "w") as log:
    log.write("=== Chat History ===\n")

    while True:
        text = input("You: ").strip()
        if text.lower() == "bye":
            print("Bot: Goodbye! 👋")
            log.write("You: bye\nBot: Goodbye! 👋\n")
            break

        if not text:
            print("Bot: Please type something!")
            continue

        try:
            results = emotion_analyzer(text)[0]
            top_emotions = sorted(results, key=lambda x: x['score'], reverse=True)[:2]

            response_parts = []
            for emo in top_emotions:
                label = emo['label']
                confidence = round(emo['score'] * 100, 2)
                emoji = emoji_map.get(label, "")
                response_parts.append(f"{label} ({confidence}%) {emoji}")

            response = " | ".join(response_parts)
            print(f"Bot: Emotions detected → {response}")

            log.write(f"You: {text}\nBot: {response}\n")
        except Exception as e:
            print(f"Bot: Oops! Something went wrong → {e}")
