odoo.define('manifiestos.hide_edit_button', function (require) {
    "use strict";

    var FormController = require('web.FormController');

    FormController.include({
        renderButtons: function () {
            this._super.apply(this, arguments);
            if (this.$buttons) {
                this.$buttons.find('.o_form_button_edit').hide();
            }
        },
    });
});