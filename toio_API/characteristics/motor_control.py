from typing import Dict, List

from bleak import BleakClient
from toio_API.utils.logging import initialize_logging

from .abstract_characteristic import AbstractCharacteristic

logger = initialize_logging(__name__)


class Motor(AbstractCharacteristic):
    """Motor characteristic.
    For more information, please refer to https://toio.github.io/toio-spec/docs/ble_motor.

    Args:
        name (str, optional): Name of toio.
            - Defaults to None.
        client (BleakClient, optional): BleakClient to connect via BLE connection.
            - Defaults to None.
    """

    def __init__(self, name: str = None, client: BleakClient = None) -> None:
        super().__init__(
            uuid="10b20102-5b3b-4571-9508-cf3efcd7bbae",
            descriptor="Motor Control",
            write=False,
            write_without_response=True,
            read=True,
            notify=True,
            name=name,
            client=client,
        )

    async def control(self, left_speed: int = 100, right_speed: int = 20) -> None:
        """Controls motor to move the toio.

        Args:
            left_speed (int, optional): Speed of left motor in [-255, 255].
                - Defaults to 100.
            right_speed (int, optional): Speed of right motor in [-255, 255].
                - Defaults to 20.
        """
        write_value = bytearray(b"\x01")
        write_value.append(1)
        write_value.append(1 if 0 <= left_speed else 2)
        write_value.append(abs(left_speed))
        write_value.append(2)
        write_value.append(1 if 0 <= right_speed else 2)
        write_value.append(abs(right_speed))

        await self._send_data(write_value)

    async def time_control(
        self, left_speed: int = 100, right_speed: int = 20, time: int = 10
    ) -> None:
        """Controls motors to move the toio for a certain time.

        Args:
            left_speed (int, optional): Speed of left motor in [-255, 255].
                - Defaults to 100.
            right_speed (int, optional): Speed of left motor in [-255, 255].
                - Defaults to 20.
            time (int, optional): Time (*10 ms) to control the motors.
                - Set it in [0, 255] and 0 is exceptionally infinite.
                - Defaults to 10.
        """
        write_value = bytearray(b"\x02")
        write_value.append(1)
        write_value.append(1 if 0 <= left_speed else 2)
        write_value.append(abs(left_speed))
        write_value.append(2)
        write_value.append(1 if 0 <= right_speed else 2)
        write_value.append(abs(right_speed))
        write_value.append(time)

        await self._send_data(write_value)

    async def target_control(
        self,
        identifier: int = 0,
        time_out: int = 5,
        movement: int = 0,
        max_speed: int = 50,
        acceleration: int = 0,
        x_coordinate: int = 700,
        y_coordinate: int = 386,
        theta: int = 90,
        theta_type: int = 0,
    ) -> None:
        """Controls the toio to the desired location on a gridmap.

        Args:
            identifier (int, optional): Identifier used in motor notification.
                - Set it in [0, 255].
                - Defaults to 0.
            time_out (int, optional): Time (s) to give up the movement.
                - Set it in [0, 255] and 0 is exceptionally 10 seconds.
                - Defaults to 5.
            movement (int, optional): How to aim destination.
                - Set 0 to rotate toio as it moves.
                - Set 1 to rotate toio as it moves without going backward.
                - Set 2 to move toio after it rotates. Defaults to 0.
            max_speed (int, optional): Maximum speed of toio in [10, 255].
                - Defaults to 50.
            acceleration (int, optional): Acceleration of toio movement.
                - Set 0 for constant speed of movement.
                - Set 1 to accelerate toio as it moves.
                - Set 2 to deaccelerate toio as it moves.
                - Set 3 to accelerate toio as it moves until midpoint and then deaccelerate it.
                - Defaults to 0.
            x_coordinate (int, optional): X coordinate of the destination.
                - Set it in [0, 65535] and 65535 is for the same as write operation.
                - Defaults to 700.
            y_coordinate (int, optional): Y coordinate of the destination.
                - Set it in [0, 65535] and 65535 is for the same as write operation.
                - Defaults to 386.
            theta (int, optional): Angle of toio after arrival at the destination with respect to x-axis.
                - Set it in [0, 131071].
                - Defaults to 90.
            theta_type (int, optional): How to change the angle of toio.
                - Set 0 for absolute angle and toio veers for less angular distance.
                - Set 1 for absolute angle and toio veers clockwise.
                - Set 2 for absolute angle and toio veers counter-clockwise.
                - Set 3 for relative angle and toio veers clockwise.
                - Set 4 for relative angle and toio veers counter-clockwise.
                - Set 5 for no angle change.
                - Set 6 for the same as write operation and toio veers for less angular distance.
                - Defaults to 0.
        """
        write_value = bytearray(b"\x03")
        write_value.append(identifier)
        write_value.append(time_out)
        write_value.append(movement)
        write_value.append(max_speed)
        write_value.append(acceleration)
        write_value.append(0)
        write_value.extend(x_coordinate.to_bytes(2, "little"))
        write_value.extend(y_coordinate.to_bytes(2, "little"))
        theta += (2 ** 13) * theta_type
        write_value.extend(theta.to_bytes(2, "little"))

        await self._send_data(write_value)

    async def targets_control(
        self,
        identifier: int = 0,
        time_out: int = 5,
        movement: int = 0,
        max_speed: int = 50,
        acceleration: int = 0,
        overwrite: int = 1,
        coordinates_thetas: List[int] = [
            (100, 100, 0, 0),
            (200, 100, 90, 0),
            (200, 200, 180, 0),
        ],
    ) -> None:
        """Controls the toio to the several desired locations on a gridmap.

        Args:
            identifier (int, optional): Identifier used in motor notification.
                - Set it in [0, 255].
                - Defaults to 0.
            time_out (int, optional): Time (s) to give up the movement.
                - Set it in [0, 255] and 0 is exceptionally 10 seconds.
                - Defaults to 5.
            movement (int, optional): How to aim destination.
                - Set 0 to rotate toio as it moves.
                - Set 1 to rotate toio as it moves without going backward.
                - Set 2 to move toio after it rotates. Defaults to 0.
            max_speed (int, optional): Maximum speed of toio in [10, 255].
                - Defaults to 50.
            acceleration (int, optional): Acceleration of toio movement.
                - Set 0 for constant speed of movement.
                - Set 1 to accelerate toio as it moves.
                - Set 2 to deaccelerate toio as it moves.
                - Set 3 to accelerate toio as it moves until midpoint and then deaccelerate it.
                - Defaults to 0.
            overwrite (int, optional): Operation for overwriting.
                - Set 0 for overwriting the operation.
                - Set 1 for adding the operation.
                - Defaults to 1.
            coordinates_thetas (List[int], optional): Coordinates, arrival angles, and the way of angle change of toio.
                - The element should be a tuple of (x_coordinate, y_coordinate, theta, theta_type).
                - The values of element should follow the same rule as those of target_control method.
                - Defaults to [(100, 100, 0, 0), (200, 100, 90, 0), (200, 200, 180, 0)].

        Raises:
            ValueError: The number of destinations can be up to 29.
        """
        if 29 < len(coordinates_thetas):
            logger.warn(
                f"[{self.name}] [{self.descriptor}] len(coordinates_thetas): {len(coordinates_thetas)}"
            )

            raise ValueError()

        write_value = bytearray(b"\x04")
        write_value.append(identifier)
        write_value.append(time_out)
        write_value.append(movement)
        write_value.append(max_speed)
        write_value.append(acceleration)
        write_value.append(0)
        write_value.append(overwrite)
        for x_coordinate, y_coordinate, theta, theta_type in coordinates_thetas:
            write_value.extend(x_coordinate.to_bytes(2, "little"))
            write_value.extend(y_coordinate.to_bytes(2, "little"))
            write_value.extend(bytearray(b"\x00\x00"))
            theta += (2 ** 13) * theta_type
            write_value.extend(theta.to_bytes(2, "little"))

        await self._send_data(write_value)

    async def acceleration_control(
        self,
        translation_speed: int = 50,
        acceleration: int = 5,
        rotation_speed: int = 15,
        rotation_direction: int = 0,
        cube_direction: int = 0,
        priority: int = 0,
        time: int = 100,
    ) -> None:
        """Controls motors to accelerate the toio for a certain time.

        Args:
            translation_speed (int, optional): The translational speed of toio in [0, 255].
                - Defaults to 50.
            acceleration (int, optional): Change in speed for 100 ms.
                - The acceleration should be [0, 255] and 0 is for constant speed.
                - Defaults to 5.
            rotation_speed (int, optional): Rotationalal speed of toio.
                - Set it in [0, 65535] and the unit is degrees/sec.
                - Defaults to 15.
            rotation_direction (int, optional): Rotationalal direction of toio.
                - Set 0 for veering clockwise.
                - Set 1 for veering counter-clockwise.
                - Defaults to 0.
            cube_direction (int, optional): Direction of toio movement.
                - Set 0 for going forward.
                - Set 1 for going backward.
                - Defaults to 0.
            priority (int, optional): Set which translational speed or rotational speed to give priority.
                - Set 0 to to give priority to the translational speed.
                - Set 1 to to give priority to the rotational speed.
                - Defaults to 0.
            time (int, optional): Time (*10 ms) to control the motors.
                - Set it in [0, 255] and 0 is exceptionally infinite.
                - Defaults to 10.
        """
        write_value = bytearray(b"\x05")
        write_value.append(translation_speed)
        write_value.append(acceleration)
        write_value.extend(rotation_speed.to_bytes(2, "little"))
        write_value.append(rotation_direction)
        write_value.append(cube_direction)
        write_value.append(priority)
        write_value.append(time)

        await self._send_data(write_value)

    def _notification_callback(self, _: int, data: bytearray) -> Dict[str, int]:
        """Decode binary information from the motor characteristic.

        Args:
            _ (int): Not used in this method.
            data (bytearray): Binary data from the motor characteristic.

        Returns:
            Dict[str, int]: Decoded information.
        """
        if data[0] == int.from_bytes(bytearray(b"\x83"), "little"):
            response = {
                "response_type": data[0],
                "identifier": data[1],
                "content": data[2],
            }
            logger.warn(f"[{self.name}] [{self.descriptor}] {response}")
            return response

        elif data[0] == int.from_bytes(bytearray(b"\x84"), "little"):
            response = {
                "response_type": data[0],
                "identifier": data[1],
                "content": data[2],
            }
            logger.info(f"[{self.name}] [{self.descriptor}] {response}")

            return response

        elif data[0] == int.from_bytes(bytearray(b"\xe0"), "little"):
            response = {
                "response_type": data[0],
                "left_speed": data[1],
                "right_speed": data[2],
            }
            logger.info(f"[{self.name}] [{self.descriptor}] {response}")

            return response

        else:
            logger.warn(f"[{self.name}] [{self.descriptor}] data[0]: {data[0]}")

            raise ValueError()
