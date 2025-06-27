def test_reexports():
    from pkn import Dict, List

    from airflow_common_operators import Dict as ADict, List as AList

    assert Dict is ADict
    assert List is AList
