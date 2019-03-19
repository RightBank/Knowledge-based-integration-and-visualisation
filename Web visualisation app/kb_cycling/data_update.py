from .utils import *
from .queries import *


# for update context data transferred from the client
def data_update(phenomenon):
    context_flag = 'same'
    context = query_resulted_in_csv(server, query_context)
    for row in context:
        if str(row.phenomenon) != phenomenon:
            context_flag = 'different'
    if context_flag == 'different':
        query_update_string = query_update_context.substitute(phenomenon=phenomenon)
        endpoint = server + '/statements'

        query_update(endpoint, query_update_string)
