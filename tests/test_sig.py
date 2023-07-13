import pytest
import api_mimic


class TestPositionalArg:
    def test_positional_args_only(self, api_with_mock_callback):
        def f(a, b, c): pass

        mimiced_api, mock_callback = api_with_mock_callback({'f': f})
        mimiced_api.f(1, 2, 3)
        mock_callback.assert_called_once_with("f", {"a":1, "b":2, "c":3})


    def test_too_many_positional_args_only(self, api_with_null_callback):
        def f(a, b, c): pass

        with pytest.raises(TypeError):
            api_with_null_callback({'f': f}).f(1, 2, 3, 4, 5)


    def test_too_few_positional_args_only(self, api_with_null_callback):
        def f(a, b, c): pass

        with pytest.raises(TypeError):
            api_with_null_callback({'f': f}).f(1)


    def test_positional_free_args(self, api_with_mock_callback):
        def f(a, b, *c): pass

        mimiced_api, mock_callback = api_with_mock_callback({'f': f})
        mimiced_api.f(1, 2, 3, 4, 5, 6)
        mock_callback.assert_called_once_with("f", {"a":1, "b":2, "c":(3,4,5,6)})


class TestAllArgTypesUsed:
    def test_no_default(self, api_with_mock_callback):
        def f(a, b, *c, d, e, **f): pass

        mimiced_api, mock_callback = api_with_mock_callback({'f': f})
        mimiced_api.f(1, 2, 3, 4, 5, e='a', d='b', f='c', g='d')
        mock_callback.assert_called_once_with("f", {"a":1, "b":2, "c":(3,4,5), "d":"b", "e":"a", "f":"c", "g":"d"})


    def test_positional_default(self, api_with_mock_callback):
        def f(a, b=6, c=5, d=4, *e, f, g, **h): pass

        mimiced_api, mock_callback = api_with_mock_callback({'f': f})
        mimiced_api.f(1, f='c', g='d', h=5, i='z')
        mock_callback.assert_called_once_with("f", {"a":1, "b":6, "c":5, "d":4, "e":(), "f":"c", "g":"d", "h":5, "i":"z"})



class TestPositionalArgWithDefaultValue:
    def test_omitted_positional_or_keyword_arg(self, api_with_mock_callback):
        def f(a, b, c=3): pass

        mimiced_api, mock_callback = api_with_mock_callback({'f': f})
        mimiced_api.f(1, 2)
        mock_callback.assert_called_once_with("f", {"a":1, "b":2, "c":3})


    def test_positional_or_keyword_arg_as_positional(self, api_with_mock_callback):
        def f(a, b, c=3): pass

        mimiced_api, mock_callback = api_with_mock_callback({'f': f})
        mimiced_api.f(1, 2, 5)
        mock_callback.assert_called_once_with("f", {"a":1, "b":2, "c":5})


    def test_positional_or_keyword_arg_as_keyword(self, api_with_mock_callback):
        def f(a, b, c=3): pass

        mimiced_api, mock_callback = api_with_mock_callback({'f': f})
        mimiced_api.f(1, 2, c=7)
        mock_callback.assert_called_once_with("f", {"a":1, "b":2, "c":7})


    def test_positional_arg_non_Set_with_keyword_arg(self, api_with_mock_callback):
        def f(a, b=3, c=4, d=5, e=6, *, f): pass

        mimiced_api, mock_callback = api_with_mock_callback({'f': f})
        mimiced_api.f(1, f='z')
        mock_callback.assert_called_once_with("f", {"a":1, "b":3, "c":4, "d":5, "e":6, "f":"z"})


    def test_postionap_arg_some_set_with_keyword_arg(self, api_with_mock_callback):
        def f(a, b=3, c=4, d=5, e=6, *, f): pass

        mimiced_api, mock_callback = api_with_mock_callback({'f': f})
        mimiced_api.f(1, 'a', 'b', f='z')
        mock_callback.assert_called_once_with("f", {"a":1, "b":"a", "c":"b", "d":5, "e":6, "f":"z"})


    def test_postionap_arg_all_set_with_keyword_arg(self, api_with_mock_callback):
        def f(a, b=3, c=4, d=5, e=6, *, f): pass

        mimiced_api, mock_callback = api_with_mock_callback({'f': f})
        mimiced_api.f(1, 'a', 'b', 'c', 'd', f='z')
        mock_callback.assert_called_once_with("f", {"a":1, "b":"a", "c":"b", "d":"c", "e":"d", "f":"z"})


    def test_with_var_positional_arg(self, api_with_mock_callback):
        def f(a, b=2, *c): pass

        mimiced_api, mock_callback = api_with_mock_callback({'f': f})
        mimiced_api.f(1)
        mock_callback.assert_called_once_with("f", {"a":1, "b":2, "c":()})

    def test_with_var_positional_arg(self, api_with_mock_callback):
        def f(a, b=2, *c): pass

        mimiced_api, mock_callback = api_with_mock_callback({'f': f})
        mimiced_api.f(1, 2, 3)
        mock_callback.assert_called_once_with("f", {"a":1, "b":2, "c":(3,)})


    def test_bad_default(self, api_with_null_callback):
        def f(a, b=2, *c): pass

        with pytest.raises(TypeError):
            api_with_null_callback({'f': f}).f(1, 2, b=3)


class TestKeywordArgs:
    def test_keyword_only_no_default_values(self, api_with_mock_callback):
        def f(*, a, b, c): pass

        mimiced_api, mock_callback = api_with_mock_callback({'f': f})
        mimiced_api.f(a=1, c=3, b=2)
        mock_callback.assert_called_once_with("f", {"a":1, "b":2, "c":3})


    def test_too_many_values(self, api_with_null_callback):
        def f(*, a, b, c): pass

        with pytest.raises(TypeError):
            api_with_null_callback({'f': f}).f(a=1, c=3)


    def test_too_few_values(self, api_with_null_callback):
        def f(*, a): pass

        with pytest.raises(TypeError):
            api_with_null_callback({'f': f}).f(a=1, c=3)


    def test_var_keyword_args(self, api_with_mock_callback):
        def f(*, a, b, **c): pass

        mimiced_api, mock_callback = api_with_mock_callback({'f': f})
        mimiced_api.f(a=1, b=2, c=3, d=4, e=5)
        mock_callback.assert_called_once_with("f", {"a":1, "b":2, "c":3,"d":4,"e":5})

    def test_kwarg_clash(self, api_with_null_callback):
        def f(a, b, **c): pass

        with pytest.raises(TypeError):
            api_with_null_callback({'f': f}).f(1, 2, b=4)



class TestKeywordArgsWithDefault:
    def test_no_values_set(self, api_with_mock_callback):
        def f(*, a, b, c=3, d=4): pass

        mimiced_api, mock_callback = api_with_mock_callback({'f': f})
        mimiced_api.f(b=2, a=1)
        mock_callback.assert_called_once_with("f", {"a":1, "b":2, "c":3, "d":4})


    def test_with_all_values_set(self, api_with_mock_callback):
        def f(*, a, b, c=3, d=4): pass

        mimiced_api, mock_callback = api_with_mock_callback({'f': f})
        mimiced_api.f(b=2, a=1, c=4, d=5)
        mock_callback.assert_called_once_with("f", {"a":1, "b":2, "c":4, "d":5})


    def test_with_some_values_set(self, api_with_mock_callback):
        def f(*, a, b, c=3, d=4): pass

        mimiced_api, mock_callback = api_with_mock_callback({'f': f})
        mimiced_api.f(b=2, a=1, d=5)
        mock_callback.assert_called_once_with("f", {"a":1, "b":2, "c":3, "d":5})


    def test_with_bad(self, api_with_null_callback):
        def f(*, a, b, c=3, d=4): pass

        with pytest.raises(TypeError):
            api_with_null_callback({'f': f}).f(a=1, c=3)
