/** @odoo-module **/
import publicWidget from '@web/legacy/js/public/public_widget';
import { jsonrpc } from "@web/core/network/rpc_service";
import { renderToFragment } from "@web/core/utils/render";

export function _chunk(array, size) {
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}
publicWidget.registry.snippet_clicking_page = publicWidget.Widget.extend({
    selector: '.dynamic_snippet',
    events: {
        'click .card': '_onClickSnippet',
    },

    _onClickSnippet: function(e){
    console.log('hi')
        var clicked_property_id = e.currentTarget.id
        window.location = `/property/${clicked_property_id}`;
    },

});

var TopSellingProperties = publicWidget.Widget.extend({
        selector: '.dynamic_snippet',

        start: function () {
            jsonrpc('/top_properties', {}).then((data) => {
            const refEl = this.$el.find("#top_properties")
            var result = _chunk(data['property_items'], 4)
            result[0].is_active = true
            const unique_id = Date.now()
            refEl.html(renderToFragment('property_management.property_snippet_carousel', {
                result,
                unique_id
            }))
            })
        }
    });
publicWidget.registry.property_list_snippet = TopSellingProperties;
return TopSellingProperties;
