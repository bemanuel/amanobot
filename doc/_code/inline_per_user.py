import sys
import time
import amanobot
from amanobot.loop import MessageLoop
from amanobot.delegate import pave_event_space, per_inline_from_id, create_open
from amanobot.namedtuple import InlineQueryResultArticle, InputTextMessageContent

class QueryCounter(amanobot.helper.InlineUserHandler, amanobot.helper.AnswererMixin):
    def __init__(self, *args, **kwargs):
        super(QueryCounter, self).__init__(*args, **kwargs)
        self._count = 0

    def on_inline_query(self, msg):
        def compute():
            query_id, from_id, query_string = amanobot.glance(msg, flavor='inline_query')
            print(self.id, ':', 'Inline Query:', query_id, from_id, query_string)

            self._count += 1
            text = '%d. %s' % (self._count, query_string)

            articles = [InlineQueryResultArticle(
                            id='abc',
                            title=text,
                            input_message_content=InputTextMessageContent(
                                message_text=text
                            )
                       )]

            return articles

        self.answerer.answer(msg, compute)

    def on_chosen_inline_result(self, msg):
        result_id, from_id, query_string = amanobot.glance(msg, flavor='chosen_inline_result')
        print(self.id, ':', 'Chosen Inline Result:', result_id, from_id, query_string)

TOKEN = sys.argv[1]  # get token from command-line

bot = amanobot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_inline_from_id(), create_open, QueryCounter, timeout=10),
])
MessageLoop(bot).run_as_thread()

while 1:
    time.sleep(10)
