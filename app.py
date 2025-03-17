import gradio as gr
import json
import openai
import os

# Load FAQs
with open('structured_faqs.json', 'r', encoding='utf-8') as f:
    faq_data = json.load(f)

# OpenAI setup
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_answer_from_gpt(question):
    prompt = "Answer based on these FAQs:\n\n"
    for category, faqs in faq_data.items():
        if faqs:
            prompt += f"{category} FAQs:\n"
            for faq in faqs:
                prompt += f"Q: {faq['question']}\nA: {faq['answer']}\n\n"
    prompt += f"Q: {question}\nA:"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()


def search_faqs(keyword):
    results = []
    for category, faqs in faq_data.items():
        for faq in faqs:
            if keyword.lower() in faq['question'].lower() or keyword.lower() in faq['answer'].lower():
                results.append(f"**Category**: {category}\n**Q**: {faq['question']}\n**A**: {faq['answer']}\n")
    return "\n".join(results) if results else "No matches found."


# Gradio Interface
with gr.Blocks(title="FAQ Bot") as demo:
    gr.Markdown("# RRA FAQ Bot")

    with gr.Tab("Ask Question"):
        question_input = gr.Textbox(label="Ask a question")
        answer_output = gr.Textbox(label="Answer", interactive=False)
        ask_btn = gr.Button("Get Answer")

    with gr.Tab("Search FAQs"):
        search_input = gr.Textbox(label="Enter keyword")
        search_output = gr.Markdown()
        search_btn = gr.Button("Search")

    ask_btn.click(
        fn=get_answer_from_gpt,
        inputs=question_input,
        outputs=answer_output
    )

    search_btn.click(
        fn=search_faqs,
        inputs=search_input,
        outputs=search_output
    )

if __name__ == "__main__":
    demo.launch()