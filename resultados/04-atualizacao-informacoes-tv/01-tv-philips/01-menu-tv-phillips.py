# python 3.11

import random
from paho.mqtt import client as mqtt_client
from consolemenu import *
from consolemenu.format import *
from consolemenu.items import *

broker = 'localhost'
port = 1883
product_id = "8002_1252_6042_1372"
# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'
username = 'user1'
password = '12345'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client, topic, filename):
    
    jsonFile = open(filename)
    msg = jsonFile.read()
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
    

def publish_digital_namaplate():
    client = connect_mqtt()
    client.loop_start()
    publish(client, product_id + '/received/digital_nameplate', 'phillips-digital-nameplate.json')
    client.loop_stop()

def publish_vendor_informations():
    client = connect_mqtt()
    client.loop_start()
    publish(client, product_id + '/received/vendor_informations', 'phillips-vendor-informations.json')
    client.loop_stop()

def publish_technical_data():
    client = connect_mqtt()
    client.loop_start()
    publish(client, product_id + '/received/technical_data', 'phillips-technical-data.json')
    client.loop_stop()

def publish_profile():
    client = connect_mqtt()
    client.loop_start()
    publish(client, product_id + '/received/profile', 'phillips-profile.json')
    client.loop_stop()

def main():
        # Change some menu formatting
    menu_format = MenuFormatBuilder().set_border_style_type(MenuBorderStyleType.HEAVY_BORDER) \
        .set_prompt("SELECT>") \
        .set_title_align('center') \
        .set_subtitle_align('center') \
        .set_left_margin(4) \
        .set_right_margin(4) \
        .show_header_bottom_border(True)
    
    # Create the menu
    menu = ConsoleMenu("Starview - Monitoramento Avançado de Televisão", 
                       "Time: Andrya Karla Oliveira da Silva \n" + 
                       "      Neyla Kelly da Silva Souza\n" + 
                       "      Max Simões dos Santos\n" + 
                       "      Jean Allison de Oliveira Nunes\n" + 
                       "      José Eduardo Lima Fernandes\n" + 
                       "      Orlewilson Bentes Maia\n" + 
                       "      William Mourão Pereira\n",
                       prologue_text="Este script possibilita publicar informações de uma TV para um servidor MQTT",
                       formatter=MenuFormatBuilder()
                            .set_title_align('center')
                            .set_subtitle_align('center')
                            .set_border_style_type(MenuBorderStyleType.DOUBLE_LINE_BORDER)
                            .show_prologue_top_border(True)
                            .show_prologue_bottom_border(True))
    
    # Create a different formatter for another submenu, so it has a different look
    submenu_formatter = MenuFormatBuilder().set_border_style_type(MenuBorderStyleType.ASCII_BORDER)

    function_publish_digital_nameplate_info = FunctionItem("Submodelo Digital Nameplate", publish_digital_namaplate)
    function_publish_vendor_informations_info = FunctionItem("Submodelo Vendor Informations", publish_vendor_informations)
    function_publish_technical_data_info = FunctionItem("Submodelo Technical Data", publish_technical_data)
    function_publish_profile_info = FunctionItem("Submodelo Profile", publish_profile)

    # Create a third submenu which uses double-line border
    submenu_tv_philips = ConsoleMenu("TV Philips",
                            prologue_text="Escolha uma opção para publicar informações no MQTT Broker de acordo o submodelo",
                            formatter=MenuFormatBuilder()
                            .set_title_align('center')
                            .set_subtitle_align('center')
                            .set_border_style_type(MenuBorderStyleType.DOUBLE_LINE_BORDER)
                            .show_prologue_top_border(True)
                            .show_prologue_bottom_border(True))
    
    submenu_tv_philips.append_item(function_publish_digital_nameplate_info)
    submenu_tv_philips.append_item(function_publish_technical_data_info)
    submenu_tv_philips.append_item(function_publish_vendor_informations_info)
    submenu_tv_philips.append_item(function_publish_profile_info)
    
    # Menu item for opening submenu 3
    submenu_item_tv_philips = SubmenuItem("TV Phillips", submenu=submenu_tv_philips)
    submenu_item_tv_philips.set_menu(menu)

    # Add all the items to the root menu
    # menu.append_item(submenu_item_2)
    menu.append_item(submenu_item_tv_philips)

    # Show the menu
    menu.start()
    menu.join()


if __name__ == "__main__":
    main()