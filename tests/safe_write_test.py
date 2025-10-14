from django.db import transaction  # type: ignore[import]
from django.contrib.auth import get_user_model  # type: ignore[import]
from typing import Any

User: Any = get_user_model()  # type: ignore
print('User count before:', User.objects.count())
try:
    with transaction.atomic():
        sid = transaction.savepoint()
        u = User.objects.create(username='temp_test_user_for_write', email='temp_write@example.com')
        print('Created temp user id:', u.id)
        print('User count inside tx:', User.objects.count())
        transaction.savepoint_rollback(sid)
        print('Rolled back savepoint')
    print('User count after rollback:', User.objects.count())
except Exception as e:  # pylint: disable=broad-except
    import traceback
    traceback.print_exc()
    print('Exception during safe write test:', e)
