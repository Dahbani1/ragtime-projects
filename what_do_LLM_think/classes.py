from typing import Optional
from ragtime.expe import QA, Chunks, Prompt, Question, WithLLMAnswer
from ragtime.generators import Prompter

class MCQAnsPptr(Prompter):
    def get_prompt(self, question:Question, chunks:Optional[Chunks] = None) -> Prompt:
        result:Prompt = Prompt()
        result.user = f"{question.text}"
        result.system = "Répond uniquement avec la lettre. Ne donne qu'une seule réponse."
        return result
    
    def post_process(self, qa:QA=None, cur_obj:WithLLMAnswer=None):
        na:str = "na"
        ans:str = cur_obj.llm_answer.text.strip() # gets the raw output from the LLM and remove blanks
        # the line below is to used to strip Claude introductory phrase even when told not to
        ans = ans.replace('La bonne réponse est ', '') if ans.startswith('La bonne réponse est ') else ans
        ans = ans[0] # keep the first character
        cur_obj.text = ans # assign this letter as the text of the current Answer being built
        transco_table:dict = qa.question.meta.get('transco', None) # try to retrieve the Transco dict associated with the current question
        transco:str = transco_table.get(ans, na) if transco_table else na # get the value associated with the letter in the Answer - "na"" if not found
        cur_obj.meta['transco'] = transco # stored the value in the Answer's meta data, key "transco"