from gemini import Suggestions_model

complaint="""
On 16/10/2024, I became a victim of a cybercrime. An unknown individual, under the
guise of naukri, contacted me through email, social media, phone call.
They employed deceitful tactics to gain my trust and subsequently obtained 
personal details. Subsequently, they utilized this information to 
identity theft. I have attached relevant evidence, including 
screenshots, emails, to support my claim. 
I request a thorough investigation into this matter and 
appropriate legal action against the perpetrators.
"""

mdl=Suggestions_model()
answer=mdl.get_suggestions(complaint)
print(answer["suggestions"])




