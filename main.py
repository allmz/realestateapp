from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.lang import Builder
from database import create_connection, create_table, add_user, get_user_by_id

Builder.load_file('realestateapp.kv')

class LoginScreen(Screen):
    username_input = StringProperty('')
    license_id_input = StringProperty('')

    def login_user(self):
        self.username_input = self.ids.username.text
        self.license_id_input = self.ids.license_id.text

        conn = create_connection('real_estate.db')
        user_id = add_user(conn, self.username_input, self.license_id_input)
        conn.close()

        if user_id:
            app = App.get_running_app()
            app.user_id = user_id
            self.manager.current = 'estate_list'
        else:
            print("Failed to add user.")

class EstateListScreen(Screen):
    def go_to_ricci_hall(self):
        self.manager.current = 'ricci_hall'

    def go_back(self):
        self.manager.transition.direction = 'right'  
        self.manager.current = 'login'

class RicciHallScreen(Screen):
    user_name = StringProperty('')
    license_id = StringProperty('')

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        conn = create_connection('real_estate.db')
        user_info = get_user_by_id(conn, app.user_id)
        conn.close()

        if user_info:
            self.user_name, self.license_id = user_info[1], user_info[2]
        else:
            print("User not found.")

    def show_agent_details(self):
        self.manager.current = 'agent'

class AgentScreen(Screen):
    agent_name = StringProperty('')
    agent_license_id = StringProperty('')

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        conn = create_connection('real_estate.db')
        agent_info = get_user_by_id(conn, app.user_id)
        conn.close()

        if agent_info:
            self.agent_name, self.agent_license_id = agent_info[1], agent_info[2]


    def go_back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'ricci_hall'

class RealEstateApp(App):
    user_id = None  

    def build(self):
        conn = create_connection('real_estate.db')
        create_table(conn)
        conn.close()

        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(EstateListScreen(name='estate_list'))
        self.sm.add_widget(RicciHallScreen(name='ricci_hall'))
        self.sm.add_widget(AgentScreen(name='agent'))
        return self.sm

if __name__ == '__main__':
    RealEstateApp().run()
