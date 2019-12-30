import traceback
import datetime as d

def error_catch_decorator(error_function):
    def wrapped_error(*args):
        try:
            error_function(*args)
        except Exception as e:
            err = traceback.format_exc()
            with open('logs_error/{}.txt'.format(d.datetime.now().strftime('%d_%m_%y-%H_%M')), 'w') as file:
                file.write('''Error is - {}\n Traceback is - ...\n{}'''.format(e, err))
            print('THE ERROR IS - {}'.format(e))
            print('ERROR LOGGING')
            traceback.print_exc()
            print('ERROR LOGGING IS DONE!')
    return wrapped_error