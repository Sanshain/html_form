class HTMLForm(forms.ModelForm):

    class Enctype:
        Default = ''
        Multipart = 'multipart/form-data'
        Text = 'text/plain'

        def __str__(self):
            return self.value

        def __init__(self, value=''):
            self.value = value


    """
    Обычная модель-форма, но наследуясь от нее, вам не нужно писать в шаблоне теги
        <form>, <input submit>, csrf-токен - все это она сделает автоматически
        а так же добавлит к форме css-класс, если он задан в конструкторе

        Добавил: возможность добавлять атрибут enctype к форме

        \sub в __init__ не должен быть равен 'def': надпись должна быть явно указана в классе формы
        предназначен только для ModelForm, не предназначен для обычных форм
    """

    def __init__(self, sub = 'def', cssclass = '', *args, **kwargs):                 # request=None,

        super(HTMLForm, self).__init__(*args, **kwargs)

        self.request = kwargs.pop('request', None)                                   # kwargs.pop('request', None)
        self.submit = sub
        self.css_class = cssclass
        self.enctype = kwargs.get('enctype','')

    @property
    def cls(self):
        return self.__class__.__name__

    def as_h(self):

        csrf_t = '<p style="color:red">Set csrf in your view \%s\</p>'%self.cls
        cssclass = format_html(u' class="{}"', self.css_class) if len(self.css_class) else ''
        enctype = ' enctype={}'.format(self.enctype) if self.enctype else ''
        submit = 'in %s not defined'%self.cls if self.submit == 'def' else self.submit

        if self.request:
			csrf_t = '<input type="hidden" name="csrfmiddlewaretoken" value="' + get_token(self.request) + '">'

        html = '<form method="post"{0}{1}>{2}'.format(cssclass, enctype, csrf_t)
        html += self.as_p() + '<input type="submit" value=%s></form>'%submit

        return mark_safe(html)

    def __unicode__(self):
        return self.as_h()



class HTMLabelForm(HTMLForm):
    """
    то же самое, что и HTMLForm, но позволяет вручную указывать тэг


    """

	# хорошо бы перенести в конструктор. Но почему не работает через эксземпляр класса так, так же непонятно. Надо пост запостить:
    tag = 'div'
    """
    Делает help_text_html невидимым и добавляет к нему класс help-text
    """
    def as_h(self):

        as_p = self._html_output(
            normal_row = u'<'+HTMLabelForm.tag+'%(html_class_attr)s>%(label)s %(field)s %(help_text)s %(errors)s</'+HTMLabelForm.tag+'>',
            error_row = u'<div class="error">%s</div>',
            row_ender = '</div>',
            help_text_html = u'<div hidden class="help-text">%s</div>',
            errors_on_separate_row = False)

        csrf_t = '<p style="color:red">Set csrf in your view</p>'
        submit = self.submit
        cssclass = format_html(u'class="{}"', self.css_class) if len(self.css_class) > 0 else ''

        if self.request != None:
            csrf_t = '<input type="hidden" name="csrfmiddlewaretoken" value="' + get_token(self.request) + '">'
        if self.submit == 'def':
        	submit = 'in_' + self.__class__.__name__ + '_notdefined'

        html = '<form method="post" '+ cssclass + '>' + csrf_t + as_p + '<input type="submit" value=' + submit + '></form>'

        return mark_safe(html)

