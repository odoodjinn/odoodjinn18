/** @odoo-module */
import { registry } from "@web/core/registry";
import { Component, useState, useRef } from "@odoo/owl";
import { useInputField } from "@web/views/fields/input_field_hook";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

class RangeSliderWidget extends Component {
    setup() {
        this.state = {
            value: this.props.record.data[this.props.name],
        };
    }
    onSliderChange(e) {
        var newValue = parseInt(event.target.value);
        this.state.value = newValue
        this.props.record.update({ [this.props.name]: newValue });
    }
}
RangeSliderWidget.template = "range_slider_widget.SliderWidgetTemplate";
RangeSliderWidget.props = {
    ...standardFieldProps,
}
RangeSliderWidget.supportedTypes = ["integer"];
registry.category("fields").add("slider", {
    component: RangeSliderWidget,
});

