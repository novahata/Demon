import g4f

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label


class ChatApp(App):

    def build(self):
        # 🔥 список для збереження всієї історії діалогу
        self.messages = []

        return super().build()

    # --- ВІДПРАВКА ПОВІДОМЛЕННЯ ---
    def send_message(self):
        user_text = self.root.ids.user_input.text.strip()

        if not user_text:
            return

        # додаємо в історію
        self.messages.append({
            "role": "user",
            "content": user_text
        })

        # показуємо в UI
        self.add_message(
            "You: " + user_text,
            color=(1, 0.647, 0, 1)
        )

        # очищаємо поле
        self.root.ids.user_input.text = ""

        # тимчасове повідомлення
        self.add_message(
            "Demon: ...",
            color=(0.5, 0.5, 0.5, 1)
        )

        # виклик без блокування UI
        Clock.schedule_once(lambda dt: self.get_response(), 0.1)

    # --- ДОДАВАННЯ ПОВІДОМЛЕННЯ ---
    def add_message(self, text, color=(0, 0, 0, 1)):
        chat_layout = self.root.ids.chat_layout

        lbl = Label(
            text=text,
            size_hint_y=None,
            halign='left',
            valign='top',
            color=color,
            font_size="16sp"
        )

        # перенос тексту
        lbl.bind(
            width=lambda instance, value: setattr(instance, 'text_size', (value, None))
        )

        # авто-висота
        lbl.bind(
            texture_size=lambda instance, value: setattr(instance, 'height', value[1])
        )

        chat_layout.add_widget(lbl)

        Clock.schedule_once(lambda dt: self.scroll_to_bottom())

    # --- СКРОЛ ---
    def scroll_to_bottom(self):
        self.root.ids.scroll.scroll_y = 0

    # --- ОТРИМАННЯ ВІДПОВІДІ ---
    def get_response(self):
        chat_layout = self.root.ids.chat_layout

        try:
            response = g4f.ChatCompletion.create(
                model="gpt-4",
                messages=self.messages   # 🔥 передаємо всю історію
            )

            # видаляємо "Bot: ..."
            if chat_layout.children:
                chat_layout.remove_widget(chat_layout.children[0])

            # додаємо відповідь в історію
            self.messages.append({
                "role": "assistant",
                "content": str(response)
            })

            # показуємо в UI
            self.add_message(
                "Demon: " + str(response),
                color=(0, 0, 0, 1)
            )

        except Exception as e:
            if chat_layout.children:
                chat_layout.remove_widget(chat_layout.children[0])

            self.add_message(
                "Error: " + str(e),
                color=(1, 0, 0, 1)
            )


if __name__ == "__main__":
    ChatApp().run()