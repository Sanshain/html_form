HtmlForm - это модифицированный вариант ModelForm для фреймворка Django


По сути это обычная модель-форма, но наследуясь от нее, не нужно писать в шаблоне теги
`<form>`, `<input submit>`, `{% csrf_token %}` - все это она сделает автоматически
а так же добавлит к форме css-класс, если он задан в конструкторе
Добавил: возможность добавлять атрибут enctype к форме
\sub в `__init__` не должен быть равен `'def'`: надпись должна быть явно указана в классе формы
предназначен только для ModelForm, не предназначен для обычных форм
    
    
    
   Применение: 
   
   class MyForm(HTMLabelForm):
    """
    Венец труда
    """
    class Meta:
      model = MyModel
      fields = ("username", "email")
      
    def __init__(self, *args, **kwargs):
      super(SignUpForm, self).__init__(*args, **kwargs)
      HTMLabelForm.tag = 'div' 
      self.submit = u'my_submit'
        
        
