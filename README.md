How to use: 
run command in terminal: pip install kivy
run command in terminal: pip install kivymd
run: python main.py

TASK 1 - display license id
```
def on_pre_enter(self, *args):
    app = App.get_running_app()
    conn = create_connection('real_estate.db')
    agent_info = get_user_by_id(conn, app.user_id)
    conn.close()

    if agent_info:
        self.agent_name, self.agent_license_id = agent_info[1], agent_info[2]
```
