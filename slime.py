from manim import *
config.disable_caching = True
import numpy as np
from scipy.ndimage import gaussian_filter, convolve

class SlimeSimulation(Scene):
    """Simulates the movement and interaction of agents in a 2D environment, visualized using Manim."""

    def construct(self):
        """Constructs the slime simulation, initializing parameters and running the simulation loop."""
        
        moveSpeed = 10  # Speed at which agents move
        deltaTime = 0.1  # Time increment for each update
        N = 1000  # Number of simulation steps
        width = 200  # Width of the simulation area
        height = int(width * 16 / 9)  # Height of the simulation area, maintaining a 16:9 aspect ratio
        DrawMap = np.zeros((width, height))  # 2D array representing the environment
        nrAgents = 700  # Number of agents in the simulation
        evaporateSpeed = 0.1  # Rate at which the environment "evaporates"
        sensorOffsetDst = 5  # Distance from the agent to the sensor center
        sensorSize = 4  # Size of the sensor area
        sensorAngleSpacing = 0.78  # Angle spacing for sensor detection
        turnSpeed = 2.5  # Speed of agent turning
        diffuseFaktor = 0.4  # Factor for diffusion in the environment

        class Agent:
            """Represents an individual agent in the simulation."""
            
            def __init__(self, pos, angle):
                """
                Initializes an agent with a position and angle.
                
                Args:
                    pos (np.array): The initial position of the agent.
                    angle (float): The initial angle of movement for the agent.
                """
                self.pos = pos  # Current position of the agent
                self.angle = angle  # Current angle of movement

        def update_agent(agent):
            """Updates the agent's position based on its current angle and checks for boundary collisions.
            
            Args:
                agent (Agent): The agent to be updated.
            """
            direction = np.array([np.cos(agent.angle), np.sin(agent.angle)])  # Calculate direction vector
            newPos = agent.pos + direction * moveSpeed * deltaTime  # Update position based on speed and direction

            # Check for boundary collisions and randomize angle if out of bounds
            if (newPos[0] < 0 or newPos[0] >= width or newPos[1] < 0 or newPos[1] >= height):
                newPos[0] = min(width - 0.01, max(0, newPos[0]))  # Constrain x position
                newPos[1] = min(height - 0.01, max(0, newPos[1]))  # Constrain y position
                agent.angle = np.random.random() * 2 * PI  # Randomize angle on collision

            agent.pos = newPos  # Update agent's position
            DrawMap[int(newPos[0]), int(newPos[1])] = 1  # Update the DrawMap to indicate agent's position
            steer(agent)  # Adjust the agent's angle based on sensor data

        def evaporate_map(DrawMap):
            """Evaporates the values in the DrawMap over time.
            
            Args:
                DrawMap (np.array): The map representing the environment.
            """
            for i in range(width):
                for j in range(height):
                    DrawMap[i, j] = max(0, DrawMap[i, j] - evaporateSpeed * deltaTime)  # Decrease values

        def diffuse(DrawMap, sigma=diffuseFaktor):
            """Applies Gaussian filtering to the DrawMap to simulate diffusion.
            
            Args:
                DrawMap (np.array): The map to be diffused.
                sigma (float): The standard deviation for Gaussian filtering.
                
            Returns:
                np.array: The diffused DrawMap.
            """
            return gaussian_filter(DrawMap, sigma=sigma)

        def sense(agent, sensorAngleOffset):
            """Senses the environment in a specified direction relative to the agent's angle.
            
            Args:
                agent (Agent): The agent performing the sensing.
                sensorAngleOffset (float): The angle offset for the sensor.
                
            Returns:
                float: The total sensed value in the direction of the sensor.
            """
            sensorAngle = agent.angle + sensorAngleOffset  # Calculate sensor angle
            sensorDir = np.array([np.cos(sensorAngle), np.sin(sensorAngle)])  # Direction of the sensor
            sensorCenter = agent.pos + sensorDir * sensorOffsetDst  # Calculate sensor center position
            total = 0.0  # Initialize total sensed value

            sensorCenter = np.clip(sensorCenter, [0, 0], [width - 1, height - 1]).astype(int)  # Ensure bounds

            # Accumulate sensed values from the sensor area
            for offsetX in range(-sensorSize, sensorSize + 1): 
                for offsetY in range(-sensorSize, sensorSize + 1): 
                    pos = sensorCenter + np.array([offsetX, offsetY])

                    # Ensure pos is within the bounds
                    if 0 <= pos[0] < width and 0 <= pos[1] < height:
                        total += DrawMap[pos[0], pos[1]]

            return total

        def steer(agent):
            """Adjusts the agent's angle based on the sensed environment.
            
            Args:
                agent (Agent): The agent whose angle is to be adjusted.
            """
            weightForward = sense(agent, 0)  # Weight in the forward direction
            weightLeft = sense(agent, sensorAngleSpacing)  # Weight to the left
            weightRight = sense(agent, -sensorAngleSpacing)  # Weight to the right

            randomSteerStrength = np.random.random()  # Random value for steering adjustments

            # Determine steering based on sensed weights
            if weightForward > weightLeft and weightForward > weightRight:
                agent.angle += 0  # Go straight
            elif weightForward < weightLeft and weightForward < weightRight:
                agent.angle += (randomSteerStrength - 0.5) * 2 * turnSpeed * deltaTime  # Randomly steer
            elif weightRight > weightLeft:
                agent.angle -= randomSteerStrength * turnSpeed * deltaTime  # Steer left
            elif weightLeft > weightRight:
                agent.angle += randomSteerStrength * turnSpeed * deltaTime  # Steer right

        def draw_draw_map(DrawMap):
            """Creates an RGB image from the DrawMap for visualization.
            
            Args:
                DrawMap (np.array): The map to be visualized.
                
            Returns:
                np.array: The RGB image representation of the DrawMap.
            """
            DrawMap = np.clip(DrawMap, 0, 1)  # Ensure values are within bounds

            height, width = DrawMap.shape
            rgb_image = np.zeros((height, width, 3), dtype=np.uint8)  # Initialize RGB image

            # Set RGB channels based on DrawMap values
            rgb_image[..., 0] = (DrawMap * 255).astype(np.uint8)
            rgb_image[..., 1] = (DrawMap * 255).astype(np.uint8)
            rgb_image[..., 2] = (DrawMap * 255).astype(np.uint8)

            return rgb_image

        # Initialize agents with random positions and angles
        agents = [Agent(np.array([np.random.random() * width, np.random.random() * height]), 
                         np.random.random() * 2 * PI) for i in range(nrAgents)]

        # Create the initial image from the DrawMap
        image1 = ImageMobject(draw_draw_map(DrawMap))
        image1.scale_to_fit_height(config.frame_height)  # Scale image to fit the scene height
        image1.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])  # Set resampling algorithm
        self.add(image1)  # Add image to the scene

        # Main simulation loop
        for _ in range(N):
            for agent in agents:
                update_agent(agent)  # Update each agent's position and angle
            DrawMap = diffuse(DrawMap)  # Apply diffusion to the DrawMap
            evaporate_map(DrawMap)  # Evaporate the values in the DrawMap

            # Create and display the new image from the updated DrawMap
            image1 = ImageMobject(draw_draw_map(DrawMap))
            image1.scale_to_fit_height(config.frame_height)  # Scale image to fit the scene height
            image1.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])  # Set resampling algorithm
            
            self.add(image1)  # Add the new image to the scene
            self.wait(deltaTime)  # Wait for the duration of deltaTime
            self.remove(image1)  # Remove the image from the scene for the next frame
