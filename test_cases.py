import quickstart
import pprint

ls = []

messages = quickstart_content.get_email_list()
for message in messages:
    ls.append(message["id"])
pprint.pprint(quickstart_content.get_email_content(ls[0]))

def test_get():
    assert len(quickstart_content.get_email_content(ls[0]))!=0

def test_trash():
    assert "TRASH" in ((quickstart_content.email_content_trash(ls[0]))["labelIds"])

def test_untrash():
    assert "UNTRASH"  not in ((quickstart_content.email_content_untrash(ls[0]))["labelIds"])

def test_batchmodify():
    res = quickstart_content.get_email_content(ls[0])
    #print(res)
    addlabel = "STARRED"
    oldlabel = "UNREAD"
    label_body = {"ids":[ls[0]],"addlabelIds":[addlabel],"removeLabelIds":[oldlabel]}
    quickstart_content.email_batch_modify(label_body)
    res_1 = (quickstart_content.get_email_content(ls[0]))
    assert addlabel in res_1['labelIds'] and oldlabel not in res_1['labelIds']
    
def test_delete():
    id = ls[0]
    print(id)
    quickstart_content.email_content_delete(ls[0])
    messages = quickstart_content.get_email_list()
    ls1 = []
    for message in messages:
        ls1.append(message["id"])
    assert id not in ls1