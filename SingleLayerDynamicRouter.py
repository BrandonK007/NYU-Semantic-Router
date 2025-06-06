from semantic_router import Route, RouteLayer
from semantic_router.encoders import OpenAIEncoder
import os
import logging

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("OPENAI_API_KEY is not set")
    exit(1)

os.environ["OPENAI_API_KEY"] = "_"

# Initialize encoder
encoder = OpenAIEncoder()

# Session and Rerouting Management
class UserSession:
    def __init__(self, user_id):
        self.user_id = user_id
        self.context = []
        self.rerouting_counter = 0

    def add_context(self, query):
        self.context.append(query)
        if len(self.context) > 10:  #Lim of 10
            self.context.pop(0)

    def increment_rerouting(self):
        self.rerouting_counter += 1

    def reset_rerouting(self):
        self.rerouting_counter = 0
user_sessions = {}

# Route definitions and their utterances
progress_report_rt = Route(
    name="progress_report",
    utterances=[
        "Can I have an update on my lab progress?",
        "How far am I in my coursework?",
        "What is my standing in the class?",
        "Can you tell me how many labs I have completed?",
        "Have I submitted all required assignments?",

        "Do I have any pending coursework?",
        "How many more labs do I need to finish?",
        "Am I on track to complete the course on time?",
        "What is my progress in this semester's coursework?",
        "How is my Benchmark 1 progress?",

        "How is my final report progress?",
        "How many labs are left for me to finish?",
        "Am I keeping pace with the course requirements?",
        "What tasks do I still need to complete to ensure I pass on time?",
        "How many lab projects have I successfully completed?",

        "Are there any pending assignments I still need to submit?",
        "Have I turned in all assignments?",
        "Are all of my labs submitted?",
        "What tasks do I need to finish to ensure I pass this course?",
        "What score do I have to get on this lab in order to maintain a passing score?",

        "What score do I need to have on my final report to maintain a passing score?",
        "What is my progress with the syllabus requirements?",
        "How many lab reports have I successfully submitted?",
        "Can you summarize how many labs ive completed?",
        "How am I doing in terms of class participation?",

        "Can you give me a timeline for my upcoming assignments?",
        "How often should I check in on my progress?",
        "What feedback do I have on my recent lab submissions?",
        "How does my performance compare to my peers?",
        "What notes has the professor placed upon my performance?",

    ],
)

problem_solve_rt = Route(
    name="problem_solve",
    utterances=[
        "I am struggling with my coursework.",
        "How can I get better grades in my labs?",
        "I need help understanding a lab experiment.",
        "Can you assist me with my project?",
        "I am finding this assignment too difficult.",

        "What can I do to improve my academic performance?",
        "How can I boost my GPA?",
        "I need guidance on solving a problem in my coursework.",
        "How can I approach this tricky lab experiment?",
        "How can I raise my academic standing this semester?",

        "What’s the best way to approach a challenging lab task?",
        "How can I better understand complex topics in my studies?",
        "What strategies can help me perform better in my lab assignments?",
        "I’m stuck on my project. Can you provide some guidance?",
        "I need clarification on a specific lab experiment.",

        "I have difficulty interpreting the lab data",
        "How can I approach complex lab scenarios more effectively?",
        "I'm not sure how to begin my lab report.",
        "Can you suggest strategies to enhance my practical lab skills?",
        "What steps can I take to connect theory with lab experiments?",

        "How can I effectively apply theoretical concepts in my lab work?",
        "How can I effectively apply practical concepts in my lab work?",
        "What are some proven methods to enhance my experimental techniques in the lab?",
        "Can you recommend ways to structure my lab report for better clarity?",
        "How do I translate abstract concepts into actionable steps for lab experiments?",

        "What strategies can I use to bridge the gap between theory and practical application?",
        "I'm struggling to transform theory into practice in my lab sessions. Any advice?",
        "What techniques can I use to improve my hands-on laboratory skills?",
        "How do I turn my research ideas into a well-structured lab report?",
        "Can you share a step-by-step approach to connecting theory with practical experiments?",

    ],
)

material_info_rt = Route(
    name="material_info",
    utterances=[
        "Where can I find additional study materials?",
        "Is there a textbook for this class?",
        "Where can I get research papers related to my lab?",
        "Can you provide some reference material for my coursework?",
        "Are there any online resources for this subject?",

        "Where can I access past lab reports?",
        "Can I find additional readings for this module?",
        "Are there any recommended study guides for this course?",
        "Where can I get supplementary notes?",
        "Can you point me to extra learning resources for this course?",

        "What are some reliable online platforms for resources in this subject?",
        "Where can I access extra notes or handouts related to our course content?",
        "Could you direct me to any study guides to enhance my understanding?",
        "Do you know if past lab reports are available for review?",
        "What is the grade distrubtion from numerical to letter",

        "Are there any online lecture recordings available for this course?",
        "Could you direct me to a course related digital library?",
        "Where can I download practice problems and exercises for this subject?",
        "Where can I access archived webinars or seminars for this class?",
        "Is there an online repository for past quizzes and exam papers?",

        "Is there a portal for accessing scholarly papers related to our coursework?",
        "Could you share a link to extended course notes and detailed outlines?",
        "Could you direct me to online platforms that offer free academic materials?",
        "Is there a central website where all course-related publications and resources are compiled?",
        "Where on Brightspace can I access professor lecture notes and recordings?",

        "Where can I download a collection of past assignments for practice?",
        "Are there any study sets with practice tests for this course section?",
        "Do you have a resource that compiles diverse learning materials for this class?",
        "Is there a website where I can view interactive learning modules for this subject?",
        "Where can I find extra visual aids like diagrams and charts to aid my understanding?",
    ],
)

mental_support_rt = Route(
    name="mental_support",
    utterances=[
        "I feel overwhelmed with my coursework.",
        "How do I develop better study habits?",
        "I am dealing with academic stress. Can you help?",
        "What can I do to avoid procrastination?",
        "I am feeling burnt out from studying too much.",

        "How can I manage my time better?",
        "I need advice on staying motivated.",
        "Do you have any tips for handling academic pressure?",
        "I’m struggling with my mental health due to my studies.",
        "How can I establish a more consistent study routine?",

        "I'm feeling exhausted from constant studying; how can I recharge?",
        "How can I keep my motivation high throughout the semester?",
        "Do you have any time management tips for balancing multiple assignments?",
        "What advice do you have for handling the pressure of exams and deadlines?",

        "What strategies can help me create a more structured study routine?",
        "How can I break the cycle of delaying my tasks and get started on my work?",
        "I'm looking for fresh ideas to keep my academic motivation alive.",
        "After nonstop studying, I feel completely drained; how can I recharge?",
        "With deadlines and exams looming, how can I better cope with the mounting stress?",

        "What tips do you have for juggling several projects without feeling overwhelmed?",
        "What practical methods can ease the pressure I'm feeling from my courses?",
        "I'm constantly anxious about upcoming tests and assignments; how can I ease this pressure?",
        "My mind feels cluttered with all the academic tasks; how can I simplify my schedule?",
        "I’m caught in a loop of stress and low motivation with my classes—what changes could help?",

        "I'm battling with self-doubt over my performance in class; any tips to build confidence?",
        "I need guidance on how to set realistic academic goals without overwhelming myself.",
        "I'm feeling perpetually swamped by assignments and exams; how can I create more breathing room?",
        "I'm at a crossroads with my study habits and need advice on how to reinvigorate my approach.",
        "My focus is slipping as I juggle multiple classes—can you suggest a plan to sharpen my concentration?",

    ],
)

# Define Route Layer
route_layer = RouteLayer(encoder=encoder, routes=[
    progress_report_rt,
    problem_solve_rt,
    material_info_rt,
    mental_support_rt,
])


# Response functions
def progress_report_guidance():
    return "Tracking your submitted labs and reviewing feedback will help ensure steady progress."


def problem_solve_guidance():
    return "Start by breaking the problem into smaller parts and focus on the key concepts."


def material_info_guidance():
    return "You can access additional study materials through the EG-UY 1004 portal and the university library."


def mental_support_guidance():
    return "If you are feeling overwhelmed, NYU provides free counseling services to help students manage stress."


def fallback_response():
    return "I'm not sure I understood that. Could you rephrase or ask something more specific?"


# Route response mapping
route_responses = {
    "progress_report": progress_report_guidance,
    "problem_solve": problem_solve_guidance,
    "material_info": material_info_guidance,
    "mental_support": mental_support_guidance,
    "fallback": fallback_response,
}

def get_user_session(user_id):
    if user_id not in user_sessions:
        user_sessions[user_id] = UserSession(user_id)
    return user_sessions[user_id]

# Expert Response Handling
def generate_expert_response(user_id, query):
    session = get_user_session(user_id)
    session.add_context(query)

    #Assign Expert
    route = route_layer(query)
    if not hasattr(route, 'name') or not route.name:
        return fallback_response()

    assigned_expert = route.name
    logging.info(f"Query: {query} assigned to expert: {assigned_expert}")

    #Query Reshaping if not Applicable to expert
    if not is_query_relevant(query, assigned_expert):
        session.increment_rerouting()
        
        if session.rerouting_counter > 3:  # Rerouting limit
            logging.warning(f"User {user_id} exceeded rerouting limit. Assigning fallback expert.")
            return fallback_response()

        reshaped_query = reshape_query(query, session.context)
        logging.info(f"Reshaped query: {reshaped_query}")
        return generate_expert_response(user_id, reshaped_query)

    #Response Generation
    session.reset_rerouting()
    return route_responses.get(assigned_expert, fallback_response)()

#On Topic Check
def is_query_relevant(query, assigned_expert):
    return True 

#Reshape Topic Check, Usage of last 3 queries to base context
def reshape_query(query, context):
    return f"{query} (Additional context: {context[-3:]})" 

def process_query(user_id, query):
    response = generate_expert_response(user_id, query)
    print(f"User {user_id}: {query}\nBot: {response}\n")

# Test sample queries
test_users = ["user0", "user1"]
test_queries = [
    "Can I have an update on my lab progress?",  # Should go to progress_report
    "I am struggling with my coursework.",  # Should go to problem_solve
    "Where can I find additional study materials?",  # Should go to material_info
    "I feel overwhelmed with my coursework.",  # Should go to mental_support
    "Tell me about black holes",  # Should trigger fallback response

]

for user_id in test_users:
    for query in test_queries:
        process_query(user_id, query)
