/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

class FieldVisibilityWidget extends Component {
    setup() {
        super.setup();
        this.onFieldChange = this.onFieldChange.bind(this);
    }

    mounted() {
        console.log('Component mounted');
        const choferElement = this.el.querySelector('[name="chofer_bd_man"]');
        console.log('choferElement:', choferElement);
        if (choferElement) {
            choferElement.addEventListener('change', this.onFieldChange);
            this.onFieldChange(); // Set initial visibility
        } else {
            console.error('Element with name "chofer_bd_man" not found');
        }
    }

    onFieldChange() {
        console.log('onFieldChange triggered');
        const choferElement = this.el.querySelector('[name="chofer_bd_man"]');
        const customField = this.el.querySelector('[name="f_firma_chofer"]');
        console.log('choferElement:', choferElement);
        console.log('customField:', customField);

        if (choferElement && customField) {
            const selectionValue = choferElement.value;
            console.log('selectionValue:', selectionValue);
            if (selectionValue === 'man') {  // Reemplaza 'man' con el valor específico que quieras
                customField.style.display = '';
            } else {
                customField.style.display = 'none';
            }
        } else {
            if (!choferElement) console.error('Element with name "chofer_bd_man" not found');
            if (!customField) console.error('Element with name "f_firma_chofer" not found');
        }
    }
}

FieldVisibilityWidget.template = 'manifiestos.FieldVisibilityWidget';
registry.category('fields').add('field_visibility', FieldVisibilityWidget);