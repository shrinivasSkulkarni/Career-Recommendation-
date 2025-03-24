import random

class RoadmapGenerator:
    def __init__(self):
        # General steps categorized by career development stages
        self.learning_steps = [
            "Learn the fundamentals of {career}",
            "Take an online course or certification in {career}",
            "Read books and articles about {career}",
            "Watch tutorials and videos on {career}",
            "Enroll in a degree or diploma program related to {career}"
        ]
        self.skill_building_steps = [
            "Work on practical projects related to {career}",
            "Practice {career} skills daily",
            "Build a portfolio showcasing your {career} work",
            "Participate in hackathons or competitions for {career}",
            "Contribute to open-source projects in {career}"
        ]
        self.networking_steps = [
            "Network with professionals in {career}",
            "Join online communities or forums for {career}",
            "Attend workshops or webinars on {career}",
            "Connect with mentors in {career}",
            "Follow industry leaders in {career} on social media"
        ]
        self.job_seeking_steps = [
            "Apply for internships or entry-level jobs in {career}",
            "Prepare a resume and cover letter for {career} roles",
            "Practice interviews for {career} positions",
            "Freelance on platforms like Upwork or Fiverr for {career}",
            "Attend career fairs and networking events for {career}"
        ]

    def generate(self, career):
        if not career or not isinstance(career, str):
            return ["Invalid career input. Please provide a valid career name."]
        
        career = career.strip().title()  # Normalize the input

        # Randomly select steps from each category
        learning_step = random.choice(self.learning_steps).format(career=career)
        skill_step = random.choice(self.skill_building_steps).format(career=career)
        networking_step = random.choice(self.networking_steps).format(career=career)
        job_step = random.choice(self.job_seeking_steps).format(career=career)

        # Combine the steps into a roadmap
        roadmap = [
            learning_step,
            skill_step,
            networking_step,
            job_step
        ]

        # Shuffle the roadmap for randomness
        random.shuffle(roadmap)

        return roadmap

# Example usage:
if __name__ == "__main__":
    generator = RoadmapGenerator()
    career = input("Enter a career: ")
    roadmap = generator.generate(career)
    print(f"Roadmap for {career}:\n" + "\n".join(roadmap))