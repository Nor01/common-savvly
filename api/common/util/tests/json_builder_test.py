from common.util.json_builder import JsonBuilder

import base64
import marshal

if __name__ == '__main__':
    f = "[{'car': '1000'}, {'rent':'500'}, {'insurance':'120'}]"
    e = base64.b64encode(f.encode('ascii'))



    print(base64.b64decode(e))

    m = JsonBuilder()
    m.set('[{"car": "1000"}, {"rent":"500"}, {"insurance":"120"}]')
    print(m.get())



    j = JsonBuilder()

    j = j.add_parameter("foo", "bar").add_parameter("crap", "4").add_parameter("crappy", "crap").add_list("what", ['this', 'is', 'a', 'test'])
    print(j.get())

    print("get_as_list: ", j.get_as_list())

    # get_as_list: [{'foo': 'bar', 'crap': '4', 'crappy': 'crap', 'what': ['this', 'is', 'a', 'test']}]

    print("to list: ", j.to_list())

    # to list:  [{"foo": "bar", "crap": "4", "crappy": "crap", "what": ["this", "is", "a", "test"]}]

    j3 = JsonBuilder()


    contact = '{"name": "Bobby Foo", "Email": "foo2@yahoo.com", "phone": "2125551212"}'
    j3.set(contact)
    print("to list: ", j3.to_list())

    # to list:  [{"name": "Bobby Foo", "Email": "foo2@yahoo.com", "phone": "2125551212"}]

    print("from_list: ", j3.from_list(j.get_as_list()))

    # from_list: [{"name": "Bobby Foo", "Email": "foo2@yahoo.com", "phone": "2125551212"},
    #             {"foo": "bar", "crap": "4", "crappy": "crap", "what": ["this", "is", "a", "test"]}]

    j2 = JsonBuilder()

    j2.set(j3.from_list(j.get_as_list()))
    print(j2.get())

    # [{"name": "Bobby Foo", "Email": "foo2@yahoo.com", "phone": "2125551212"},
    #  {"foo": "bar", "crap": "4", "crappy": "crap", "what": ["this", "is", "a", "test"]}]



    j4 = JsonBuilder()
    contact = '{"name": "Bobby Foo", "Email": "foo2@yahoo.com", "phone": "2125551212"}'
    j4.set(contact)

    j4.update_after_set("foo", "bar")

    print("just get: ", j4.get())
    print("get as list: ", j4.get_as_list())

