<template id="pos_model_extend">
  <t t-extend="PosModel">
    <xpath expr="//function[name='_get_partner_info']" position="inside">
      <t t-set="partner_info" t-value="super._get_partner_info(partner_id)"/>
      <t t-set="custom_fields" t-value="partner_info.custom_fields"/>
      <t t-set="partner_info" t-value="{...partner_info, custom_fields: custom_fields}"/>
    </xpath>
  </t>
</template>