from spacy.matcher import Matcher
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize the Matcher with the spaCy vocabulary
matcher = Matcher(nlp.vocab)

# Define a pattern for job titles (e.g., "data scientist", "software engineer")
job_titles = ["data scientist", "software engineer", "marketing manager"]

# Create matcher rules for job titles
for title in job_titles:
    pattern = [{"LOWER": w} for w in title.split()]
    matcher.add("JOB_TITLE", [pattern])

# Sample text
text = "Jane works as a Data Scientist at Google in the technology sector."
doc = nlp(text)

# Apply matcher to the doc
matches = matcher(doc)

# Extract job titles
for match_id, start, end in matches:
    span = doc[start:end]
    print("Job Title:", span.text)
