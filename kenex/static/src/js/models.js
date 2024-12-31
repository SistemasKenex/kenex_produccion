odoo.define('kenex.pos_attributes', function (require) {
    "use strict";

    const {ResPartner} = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');

    const PosAttributesResPartner = (ResPartner) => class PosAttributesResPartner extends ResPartner {
        constructor() {
            super(...arguments);
            this.test = this.res.partner.it_cedula_cliente_id;
        }
    };

    Registries.Model.extend(ResPartner, PosAttributesResPartner);
});



/** @odoo-module */
// import {PosGlobalState} from 'point_of_sale.models';
// import Registries from 'point_of_sale.Registries';
// console.log ('entre en models')
// const AgePosGlobalState = (PosGlobalState) => class AgePosGlobalState extends PosGlobalState{
    
//     async _processData(loadedData){
//         console.log ('despues de async')
//         await super._processData(...arguments);
//         console.log ('despues de await')
//         this.it_cedula_cliente_id = loadedData['res.partner'];
//         console.log ('despues de this.it_cedula_cliente_id ')
//         console.log (this.it_cedula_cliente_id)
//         console.log ('despues de console log del this.it_cedula_cliente_id ')
//     }
// }
// Registries.Model.extend(PosGlobalState, AgePosGlobalState);

