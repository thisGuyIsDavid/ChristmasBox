import random
import time
from gpiozero import Button
import serial

from ChristmasLights import ChristmasLights


class SerialMusicPlayer:

    def __init__(self, is_test=False):
        self.christmas = ChristmasLights()
        self.is_test = is_test
        self.is_playing = False
        if self.is_test:
            self.serial = self.get_test_serial()
        else:
            self.serial = serial.Serial(port='/dev/ttyS0', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=5)
        self.set_up()

        self.stop_button = Button(27)
        self.skip_button = Button(22)
        self.blank_space_button = Button(23)

    def set_up(self):
        self.stop_playback()
        self.set_volume()
        self.set_up_lights()

    def set_up_lights(self):
        self.christmas.light_traditional()
        print('lights set')
        self.christmas.light_tree()
        self.christmas.light_star()

    def get_test_serial(self):
        class TestSerial:
            iterator = 0

            def write(self, message):
                self.iterator = 0

            def read(self):
                print("music", self.iterator)
                self.iterator += 1
                return "".encode('utf-8')

        return TestSerial()

    @staticmethod
    def convert_dfplayer_response_to_hex(received_bytes):
        converted_string = received_bytes.hex()
        for i in range(int(len(converted_string) / 20)):
            single_message = converted_string[i*20: (i*20) + 20]
            single_message_array = []
            for x in range(20):
                two_characters = single_message[x*2:(x*2) + 2]
                if two_characters != '':
                    single_message_array.append(single_message[x*2:(x*2) + 2])
            print(single_message_array)

    @staticmethod
    def generate_command(command_one, parameter_1, parameter_2):
        """
        DFPlayer requires a special command set.
        Found though https://github.com/DFRobot/DFRobotDFPlayerMini/blob/master/doc/FN-M16P%2BEmbedded%2BMP3%2BAudio%2BModule%2BDatasheet.pdf
        :param command_one: Hexadecimal command for DF Player.
        :param parameter_1: Command param from above URL.
        :param parameter_2: Command param from above URL.
        :return: DFPlayer compatible code.
        """

        start_byte = 0x7E
        version_byte = 0xFF
        command_length = 0x06
        end_byte = 0xEF
        feedback = 0x01

        #   generate checksum.
        checksum = 65535 + -(version_byte + command_length + command_one + feedback + parameter_1 + parameter_2) + 1

        #   checksum is the high byte and low bite of the checksum.
        high_byte, low_byte = divmod(checksum, 0x100)

        array_of_bytes = [start_byte, version_byte, command_length, command_one, feedback, parameter_1, parameter_2, high_byte, low_byte, end_byte]

        command_bytes = bytes(array_of_bytes)
        return command_bytes

    def send_command(self, command):
        print('sending', command)

        self.serial.write(command)
        time.sleep(0.05)
        message = self.serial.readline()
        self.convert_dfplayer_response_to_hex(message)

    def stop_playback(self):
        self.send_command(self.generate_command(0x16, 0x00, 0x00))

    def set_volume(self, volume_level=15):
        self.send_command(self.generate_command(0x06, 0x00, int(volume_level)))

    def play_track(self, track_number):
        self.send_command(self.generate_command(0x12, 0x00, int(track_number)))

    def play_blank_space(self):
        pass

    def play(self, track_number):
        #   if something is already playing, return.
        if self.is_playing:
            return

        #   send the play command to the DFPlayer.
        self.play_track(track_number)

        #   set the is_playing variable.
        self.is_playing = True

        play_start = time.time()

        tick_count = 0
        while self.is_playing:
            #   read output. DFPlayer will return byte array when it completes.
            message = self.serial.readline()
            self.is_playing = len(bytearray(message)) == 0

            #   sleep to avoid overloading connection.
            time.sleep(0.02)

            if self.stop_button.is_pressed:
                print('stop_button')

            if self.skip_button.is_pressed:
                print('skip button')

            if self.blank_space_button.is_pressed:
                print('blank space')

            self.christmas.twinkle_tree(tick_count)

            #   if testing, don't go longer than 3 seconds.
            if self.is_test and (time.time() - play_start) > 3:
                break
            tick_count += 1

        #   set the is_playing variable.
        self.is_playing = False

    def play_all(self):
        try:
            while True:
                track_number = random.randint(2, 160)
                self.play(track_number)
            pass
        except KeyboardInterrupt:
            #   stop any playback
            self.stop_playback()



if __name__ == '__main__':
    serial_music_player = SerialMusicPlayer()
