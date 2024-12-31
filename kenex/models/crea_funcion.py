from odoo import models, fields, api

class KcreaFuncion(models.Model):
    _name = 'kcrea.funcion'
    _description = 'Crea Funcionesa'
    _auto = False
    
    company_id     = fields.Many2one('res.company', string='Compania', default=lambda self: self.env.user.company_id, readonly=True)
    name           = fields.Char('Sistema')

    def btn_secuencia(self):
      #################################################################################
        query= """delete from kcrea_funcion;
                  drop  SEQUENCE nro_funcion;
                  CREATE    SEQUENCE nro_funcion
                  START WITH 1
                  INCREMENT BY 1;
                  insert into kcrea_funcion values (nextval('nro_funcion'),4,2,2,'***********Funciones Creadas************','2024-09-06','2024-09-06');  """
        self.env.cr.execute(query)
        
        query = """insert into kcrea_funcion values 
        (nextval('nro_funcion'),4,2,2,'Generada la Secuencia (nro_funcion) en la Base de Datos'||' El dia: '|| to_char(CURRENT_TIMESTAMP, 'DD-MM-YYYY HH24:MI:SS'),'2024-09-06','2024-09-06');"""
        self.env.cr.execute(query)

    def btn_generar(self):
#################################################################################      
        query = """ DROP FUNCTION IF EXISTS public.f_meta_comision_tienda(integer, date, date);
                    CREATE OR REPLACE FUNCTION public.f_meta_comision_tienda(
	                  p_company_id integer,
	                  p_fecha_desde date,
	                  p_fecha_hasta date)
                    RETURNS double precision
                    LANGUAGE 'plpgsql'
                    COST 100
                    VOLATILE PARALLEL UNSAFE
                    AS $BODY$
                    --
                    DECLARE
                    w_bono numeric := 0;
                    reg           record;
                    --
                    -- Declaracion  de Cursores
                    --
                    --
                    BEGIN
                    --
                    FOR reg IN 
                        (select  bd.company_id  ,
	                               po.employee_id ,
	                             bd.meta    meta,
			                     bd.monto_meta monto_meta,
	                             sum(pol.qty) vendido
  	                       from kbono_detalle bd,
	                            kbono_comisiones bc,
			                    pos_order po,
			                    pos_order_line pol,
	                            pos_config pc
	                    where bd.company_id     = p_company_id
		                  and bd.company_id     = bc.company_id
	                      and bc.company_id     = po.company_id
		                  and po.company_id     = pol.company_id
	                      and po.company_id     = pc.company_id
	                      and po.session_id     = pc.id
	                      and pc.warehouse_id   = bd.warehouse_id
	                      and bc.id             = bd.codigo_bono_id
		                  and po.id             = pol.order_id
		                  and pol.product_id    = bd.product_id
		                  and po.date_order between  bc.fechadesde  and  bc.fechahasta
	                      and po.date_order BETWEEN  p_fecha_desde AND p_fecha_hasta
	                    group by  bd.company_id,po.employee_id,bd.meta, bd.monto_meta)
                    LOOP
                      IF reg.vendido >= reg.meta THEN
                        update kdetalle_comisiones_tienda set monto_meta = reg.monto_meta,
	                                        comision_descuento_ventas = comision_descuento_ventas + reg.monto_meta
                         where company_id = reg.company_id
	                       and vendedor_id = reg.employee_id
	                       and fechadesde >= p_fecha_desde  
	                       and fechahasta <=  p_fecha_hasta;
                      END IF;
                    END LOOP;
                      RETURN w_bono;
                    END;
                    $BODY$;
                ALTER FUNCTION public.f_meta_comision_tienda(integer, date, date)
                OWNER TO odoo;
        """
        self.env.cr.execute(query)
        
        query = """insert into kcrea_funcion values 
        (nextval('nro_funcion'),4,2,2,'Generada la Function f_meta_comision_tienda en la Base de Datos'||' El dia: '|| to_char(CURRENT_TIMESTAMP, 'DD-MM-YYYY HH24:MI:SS'),'2024-09-06','2024-09-06');"""
        self.env.cr.execute(query)
#################################################################################        
        query= """ DROP FUNCTION IF EXISTS public.f_bono_comision(integer, integer, integer, integer, date, date);
                    CREATE OR REPLACE FUNCTION public.f_bono_comision(
                      p_company_id integer,
                      p_order_id integer,
                      p_vendedor_id integer,
                      p_product_id integer,
                      p_fecha_desde date,
                      p_fecha_hasta date)
                        RETURNS double precision
                        LANGUAGE 'plpgsql'
                        COST 100
                        VOLATILE PARALLEL UNSAFE
                    AS $BODY$
                    --
                    DECLARE
                    w_bono numeric := 0;
                    reg           record;
                    --
                    -- Declaracion  de Cursores
                    --
                    --
                    BEGIN
                    --
                    FOR reg IN 
                        (select 
                        nextval('SECUENCIA_BONO')         cod_bono, 
                        so.company_id                     compania,
                          so.name                           documento,
                        sol.salesman_id                   vendedor,
                        bd.warehouse_id                   almacen,
                        bd.product_id                     product_id,
                        sol.product_uom_qty               pedido,
                        bd.monto_bono                     monto_bono,
                        bd.meta                           meta,
                          bc.descripcion                    descripcion, 
                        so.date_order                     fecha_orden ,
                        bc.fechadesde                     fecha_desde,  
                        bc.fechahasta                     fecha_hasta,
                        sol.product_uom_qty * bd.monto_bono calculo_bono
                          from kbono_detalle bd,
                              kbono_comisiones bc,
                          sale_order so,
                          sale_order_line sol
                        where bd.company_id     = p_company_id
                        and bd.company_id     = bc.company_id
                          and bc.company_id     = so.company_id
                        and so.company_id     = sol.company_id
                          and so.warehouse_id   = bd.warehouse_id
                          and bc.id             = bd.codigo_bono_id
                        and so.id             = p_order_id 
                        and sol.salesman_id   = p_vendedor_id
                        and so.id             = sol.order_id
                        and sol.product_id    = p_product_id
                        and sol.product_id    = bd.product_id
                        and so.date_order between  bc.fechadesde  and  bc.fechahasta
                          and so.date_order BETWEEN p_fecha_desde AND p_fecha_hasta   
                    )
                      
                      LOOP
                          w_bono := reg.calculo_bono;
                        --
                        INSERT INTO public.kbono_calculo
                        (id,
                        company_id,
                        vendedor,
                        producto,
                        almacen,
                        pedido,
                        monto_bono,
                        meta,
                        calculo_bono,
                        create_uid,
                        write_uid,
                        documento,
                        descripcion,
                        fecha_orden,
                        fechadesde,
                        fechahasta,
                        create_date,
                        write_date)
                        values
                        (reg.cod_bono, 
                          reg.compania,
                          reg.vendedor,
                          reg.product_id,
                          reg.almacen,
                          reg.pedido,
                          reg.monto_bono,
                          reg.meta,
                          reg.calculo_bono,
                          2,
                          2,
                              reg.documento,
                          reg.descripcion, 
                          reg.fecha_orden ,
                          reg.fecha_desde,  
                            reg.fecha_hasta,
                          CURRENT_DATE,
                          CURRENT_DATE);
                      END LOOP;
                      RETURN w_bono;
                    END;
                    $BODY$;

                    ALTER FUNCTION public.f_bono_comision(integer, integer, integer, integer, date, date)
                        OWNER TO odoo;"""
        self.env.cr.execute(query)
        
        query = """insert into kcrea_funcion values 
        (nextval('nro_funcion'),4,2,2,'Generada la Function f_bono_comision en la Base de Datos'||' El dia: '|| to_char(CURRENT_TIMESTAMP, 'DD-MM-YYYY HH24:MI:SS'),'2024-09-06','2024-09-06');"""
        self.env.cr.execute(query)
#################################################################################        
        query= """  DROP FUNCTION IF EXISTS public.f_bono_comision_tienda(integer, date, date);
                      CREATE OR REPLACE FUNCTION public.f_bono_comision_tienda(
                        p_company_id integer,
                        p_fecha_desde date,
                        p_fecha_hasta date)
                          RETURNS double precision
                          LANGUAGE 'plpgsql'
                          COST 100
                          VOLATILE PARALLEL UNSAFE
                      AS $BODY$
                      --
                      DECLARE
                      w_bono numeric := 0;
                      reg           record;
                      --
                      -- Declaracion  de Cursores
                      --
                      --
                      BEGIN
                      --
                      FOR reg IN 
                          (select  bd.company_id  ,
                                po.employee_id  ,	 
                                sum(pol.qty * bd.monto_bono) calculo_bono
                            from kbono_detalle bd,
                                kbono_comisiones bc,
                            pos_order po,
                            pos_order_line pol,
                                pos_config pc
                          where bd.company_id     = p_company_id
                          and bd.company_id     = bc.company_id
                            and bc.company_id     = po.company_id
                          and po.company_id     = pol.company_id
                            and po.company_id     = pc.company_id
                            and po.session_id     = pc.id
                            and pc.warehouse_id   = bd.warehouse_id
                            and bc.id             = bd.codigo_bono_id
                          and po.id             = pol.order_id
                          and pol.product_id    = bd.product_id
                          and po.date_order between  bc.fechadesde  and  bc.fechahasta
                            and po.date_order BETWEEN  p_fecha_desde  AND  p_fecha_hasta
                            group by  bd.company_id,po.employee_id)
                        
                        LOOP
                        update kdetalle_comisiones_tienda set bono = reg.calculo_bono,
                                                          comision_descuento_ventas = comision_descuento_ventas + reg.calculo_bono
                          where company_id = reg.company_id
                          and vendedor_id = reg.employee_id
                          and comision_descuento_ventas > 0
                          and fechadesde >= p_fecha_desde  
                          and fechahasta <=  p_fecha_hasta;
                        END LOOP;
                        RETURN w_bono;
                      END;
                      $BODY$;

                      ALTER FUNCTION public.f_bono_comision_tienda(integer, date, date)
                          OWNER TO odoo;"""
        self.env.cr.execute(query)
        
        query = """insert into kcrea_funcion values 
        (nextval('nro_funcion'),4,2,2,'Generada la Function f_bono_comision_tiend en la Base de Datos'||' El dia: '|| to_char(CURRENT_TIMESTAMP, 'DD-MM-YYYY HH24:MI:SS'),'2024-09-06','2024-09-06');"""
        self.env.cr.execute(query)
#################################################################################
        query= """ DROP FUNCTION IF EXISTS public.f_busca_devolucion(integer, character, integer);
                        CREATE OR REPLACE FUNCTION public.f_busca_devolucion(
                          p_company_id integer,
                          p_pedido character,
                          p_product_id integer)
                            RETURNS numeric
                            LANGUAGE 'plpgsql'
                            COST 100
                            VOLATILE PARALLEL UNSAFE
                        AS $BODY$
                        --
                        DECLARE
                        w_dv float;
                        w_docu varchar;
                        reg           record;
                        --
                        -- Declaracion  de Cursores
                        --
                        --
                        BEGIN
                        FOR reg IN (SELECT  am.name AS documento_origen,
                                      DEBIT AS total_devolucion
                                      FROM  account_move am, 
                                      account_move_line aml, 
                                      product_product p
                                    WHERE am.company_id = p_company_id
                                AND am.company_id = aml.company_id
                                AND am.id = aml.move_id
                                      AND am.invoice_origin = p_pedido
                                AND aml.product_id = p_product_id
                                      AND aml.product_id = p.id
                                      AND am.move_type = 'out_refund') 
                            
                          LOOP
                                w_dv    := reg.total_devolucion;
                          END LOOP;
                          RETURN w_dv;
                        END;
                        $BODY$;

                        ALTER FUNCTION public.f_busca_devolucion(integer, character, integer)
                            OWNER TO odoo;
                        """
        self.env.cr.execute(query)
        
        query = """insert into kcrea_funcion values 
        (nextval('nro_funcion'),4,2,2,'Generada la Function f_busca_devolucion en la Base de Datos'||' El dia: '|| to_char(CURRENT_TIMESTAMP, 'DD-MM-YYYY HH24:MI:SS'),'2024-09-06','2024-09-06');"""
        self.env.cr.execute(query)
#################################################################################
        query= """ DROP FUNCTION IF EXISTS public.f_busca_doc_orig_devolucion(integer, character, integer);
                        CREATE OR REPLACE FUNCTION public.f_busca_doc_orig_devolucion(
                          p_company_id integer,
                          p_pedido character,
                          p_product_id integer)
                            RETURNS character varying
                            LANGUAGE 'plpgsql'
                            COST 100
                            VOLATILE PARALLEL UNSAFE
                        AS $BODY$
                        --
                        DECLARE
                        w_docu varchar;
                        reg           record;
                        --
                        -- Declaracion  de Cursores
                        --
                        --
                        BEGIN
                        FOR reg IN (SELECT  am.name AS documento_origen
                                      FROM  account_move am, 
                                      account_move_line aml, 
                                      product_product p
                                    WHERE am.company_id = p_company_id
                                AND am.company_id = aml.company_id
                                AND am.id = aml.move_id
                                      AND am.invoice_origin = p_pedido
                                AND aml.product_id = p_product_id
                                      AND aml.product_id = p.id
                                      AND am.move_type = 'out_refund') 
                            
                          LOOP
                              w_docu    := reg.documento_origen;
                          END LOOP;
                          RETURN w_docu;
                        END;
                        $BODY$;

                        ALTER FUNCTION public.f_busca_doc_orig_devolucion(integer, character, integer)
                            OWNER TO odoo;
                        """
        self.env.cr.execute(query)
        
        query = """insert into kcrea_funcion values 
        (nextval('nro_funcion'),4,2,2,'Generada la Function f_busca_doc_orig_devolucion en la Base de Datos'||' El dia: '|| to_char(CURRENT_TIMESTAMP, 'DD-MM-YYYY HH24:MI:SS'),'2024-09-06','2024-09-06');"""
        self.env.cr.execute(query)
#################################################################################
        query= """ DROP FUNCTION IF EXISTS public.f_calcula_comision(integer, numeric, numeric, integer, integer, integer);
                      CREATE OR REPLACE FUNCTION public.f_calcula_comision(
                        p_company_id integer,
                        p_precio_venta numeric,
                        p_monto_linea numeric,
                        p_marca_id integer,
                        p_pricelist_id integer,
                        p_order_id integer)
                          RETURNS numeric
                          LANGUAGE 'plpgsql'
                          COST 100
                          VOLATILE PARALLEL UNSAFE
                      AS $BODY$
                      DECLARE
                        --
                        -- Declaracion  de Cursores
                        --
                        --
                          C_Precio_TI CURSOR  FOR
                            SELECT so.name,a.company_id,a.pricelist_id  tipo_precio, 
                                c.fixed_price   precio,
                                a.porc_comision porcentaje
                              FROM kporcentaje_marca a, 
                                product_pricelist b, 
                                product_pricelist_item c,
                              sale_order_line d,
                              product_product e,
                              sale_order so
                            WHERE a.company_id  in (4,5)
                            AND a.company_id      = p_company_id
                              AND a.marca_id        =  p_marca_id
                            AND a.company_id      = d.company_id 
                            AND a.company_id      = so.company_id 
                            AND d.product_id      = e.id
                            AND e.product_tmpl_id = c.product_tmpl_id
                              AND a.pricelist_id    = b.id
                              AND b.id              = c.pricelist_id
                            AND so.id             = d.order_id
                            AND so.id             = p_order_id
                              ORDER BY c.fixed_price ; 

                        --
                        reg refcursor;
                        --
                        Comision   numeric :=0; 
                          Precio_Ant numeric;
                          Comi_Ant   numeric;
                          vmonto_comision numeric;
                        --
                      BEGIN
                        For I In C_Precio_TI Loop
                          -- Si El Precio Vendido Es Igual Al Precio Real */
                          If p_precio_venta = I.Precio Then
                              If p_precio_venta = Precio_Ant Then
                                Comision := p_monto_linea * (I.porcentaje/100);
                              Else
                                  Precio_Ant := I.Precio;
                                  Comi_Ant   := I.porcentaje;
                                  Comision   := p_monto_linea * (I.porcentaje/100);
                              End If;
                            -- Si El Precio Vendido Es Mayor Al Precio Real
                          Elsif p_precio_venta > I.Precio Then
                            If p_precio_venta = Precio_Ant Then
                                Comision := p_monto_linea * (Comi_Ant/100);
                              Else
                                Comision := p_monto_linea * (I.porcentaje/100);
                              End If;
                            -- Si El Precio Vendido Es Menor Al Precio Real
                          Elsif p_precio_venta < I.Precio  Then
                              --  RAISE NOTICE '%', FORMAT('6) Si El Precio Vendido Es menos Al Precio REal orden=%s  venta=%s y precio=%s',I.name, p_precio_venta, I.Precio );
                              -- Comision := 0;
                            Comision := p_monto_linea * (Comi_Ant/100);
                          End If;
                          Precio_Ant := I.Precio;
                            Comi_Ant := I.porcentaje;
                        End Loop;
                        --
                        -- Retorna el monto de la comision
                        --
                        RETURN Comision;
                        --	
                      END;
                      $BODY$;

                      ALTER FUNCTION public.f_calcula_comision(integer, numeric, numeric, integer, integer, integer)
                          OWNER TO odoo;
                      """
        self.env.cr.execute(query)
        
        query = """insert into kcrea_funcion values 
        (nextval('nro_funcion'),4,2,2,'Generada la Function f_calcula_comision en la Base de Datos'||' El dia: '|| to_char(CURRENT_TIMESTAMP, 'DD-MM-YYYY HH24:MI:SS'),'2024-09-06','2024-09-06');"""
        self.env.cr.execute(query)
#################################################################################
        query= """ DROP FUNCTION IF EXISTS public.f_cantidad_ventas_articulos(integer, character varying);
                      CREATE OR REPLACE FUNCTION public.f_cantidad_ventas_articulos(
                        p_product_id integer,
                        p_state character varying)
                          RETURNS numeric
                          LANGUAGE 'plpgsql'
                          COST 100
                          VOLATILE PARALLEL UNSAFE
                      AS $BODY$
                      --
                      DECLARE
                      w_cantida integer := 0;
                      reg                record;
                      --
                      -- Declaracion  de Cursores
                      --
                      --
                      BEGIN
                      FOR reg IN (SELECT SUM(sol.product_uom_qty) AS cantidad
                                  FROM sale_order_line sol,
                                        sale_order so, 
                                        product_template p
                                  WHERE sol.order_id = so.id
                                    AND p.id         = sol.product_id 
                                    AND P.ID         = p_product_id
                                    AND so.state     = p_state
                                    AND so.date_order >= to_date('0101'||EXTRACT(YEAR FROM NOW()), 'DDMMYYYY')
                                    AND so.date_order <= NOW()
                          
                          )
                          
                        LOOP
                              w_cantida := reg.cantidad;
                        END LOOP;
                        RETURN w_cantida;
                      END;
                      $BODY$;

                      ALTER FUNCTION public.f_cantidad_ventas_articulos(integer, character varying)
                          OWNER TO odoo;
                      """
        self.env.cr.execute(query)
        
        query = """insert into kcrea_funcion values 
        (nextval('nro_funcion'),4,2,2,'Generada la Function f_cantidad_ventas_articulos en la Base de Datos'||' El dia: '|| to_char(CURRENT_TIMESTAMP, 'DD-MM-YYYY HH24:MI:SS'),'2024-09-06','2024-09-06');"""
        self.env.cr.execute(query)
#################################################################################
        query= """ DROP FUNCTION IF EXISTS public.f_comision_mayor_nc(integer, date, date);
                    CREATE OR REPLACE FUNCTION public.f_comision_mayor_nc(
                      p_company_id integer,
                      p_fecha_desde date,
                      p_fecha_hasta date)
                        RETURNS void
                        LANGUAGE 'plpgsql'
                        COST 100
                        VOLATILE PARALLEL UNSAFE
                    AS $BODY$
                    DECLARE
                      --
                      -- Declaracion  de Cursores
                      --
                      --
                        C_LINEAS_VENTAS CURSOR  FOR
                        SELECT o.company_id     ,
                            o.id             ,
                          o.name           ,
                          o.partner_id     ,
                            l.salesman_id    ,
                            l.product_id     ,
                            l.product_uom_qty,
                            l.price_subtotal ,
                            l.price_total ,
                              l.price_unit     ,
                          o.date_order     ,
                          case
                              when l.it_product_pricelist_id is null then o.pricelist_id
                          else
                          l.it_product_pricelist_id
                          end                                                          precio_lista,
                          pat.id                                                       marca,
                            o.margin                                                     margen,
                          (o.margin/o.amount_untaxed)*100                              porc_margen ,
                          case
                          when f_busca_devolucion(o.company_id,o.name,l.product_id) > 0 then 
                          0
                          else
                          f_bono_comision(o.company_id , o.id         , l.salesman_id,
                                              l.product_id , p_fecha_desde, p_fecha_hasta) 
                          end                                                           bono_comision,
                          f_busca_devolucion(o.company_id,o.name,l.product_id)          devolucion,
                          f_busca_doc_orig_devolucion(o.company_id,o.name,l.product_id) doc_orig_dev							 
                          FROM sale_order     o,
                              sale_order_line  l, 
                          product_product pp,
                          product_template pt,
                          PRODUCT_TEMPLATE_ATTRIBUTE_LINE PTA,
                          product_attribute pat ,
                          account_move   ac
                        WHERE o.company_id = p_company_id
                          AND o.company_id = l.company_id
                        and o.company_id = ac.company_id
                        and o.name   = ac.invoice_origin
                        and ac.reversed_entry_id is not null
                        AND o.id         = l.order_id
                        and l.product_id = pp.id
                        and pp.product_tmpl_id = pt.id 
                        AND pt.id =  pta.product_tmpl_id
                        and pta.attribute_id = pat.id
                        and ac.date   between p_fecha_desde and p_fecha_hasta
                        AND o.margin <> 0
                        AND l.price_total <> 0
                        AND l.product_uom_qty = l.qty_delivered;
                      --
                      reg            refcursor;
                      w_comision     numeric;
                      w_category_id  integer;
                      w_id           integer;
                      --
                    BEGIN
                      FOR reg IN C_LINEAS_VENTAS LOOP
                        --
                        -- Se realiza el calculo de la Comision
                        -- Retorna el monto de la comision
                          -- 
                        --w_category_id := f_busca_categoria( p_company_id => reg.company_id,
                        --                                   p_product_id => reg.product_id);
                        --
                        --w_category_id := f_get_category_id(reg.product_id);
                        --w_category_id := f_marca(1);
                        w_category_id := reg.marca;

                        w_comision := f_calcula_comision(
                                                          p_company_id    => reg.company_id  ,
                                                          p_precio_venta  => reg.price_unit  ,
                                                          p_monto_linea   => reg.price_total ,
                                                          p_marca_id      => w_category_id   ,
                                                          p_pricelist_id  => reg.precio_lista,
                                                        p_order_id      => reg.id
                                                        );

                          IF w_comision != 0 THEN
                            --IF f_busca_devolucion(reg.company_id,reg.name,reg.product_id) > 0 THEN
                          --   w_comision = 0;
                          --END IF;
                            select nextval('detalle_id_seq') into w_id;
                          INSERT INTO public.kdetalle_comisiones
                          ( id            ,	
                          create_uid     , 	
                          write_uid      , 
                          order_id       , 
                          vendedor_id    , 
                          cliente_id     ,	
                          pricelist_id   ,
                          marca_id       , 
                          fechadesde     , 
                          fechahasta     , 
                          date_order     ,
                          create_date    ,
                          write_date     ,
                          price_total    , 	   
                          porcentaje     , 		
                          porc_comision  ,
                          margen         ,
                          porc_margen    ,
                          precio_base    ,
                          bono_comision  ,
                          tot_bono_comision,
                          company_id,
                          devolucion,
                          doc_orig_dev,
                          name)
                          VALUES
                          (w_id           , 
                          1              ,	
                          1              , 
                          reg.id         ,
                          reg.salesman_id,
                          reg.partner_id,
                          reg.precio_lista,  
                          w_category_id  ,
                          p_fecha_desde  ,
                          p_fecha_hasta  ,
                            reg.date_order ,
                          current_date   ,
                          current_date   ,
                          reg.price_total  * -1,	
                          ((w_comision/reg.price_total)  * 100) * -1,  
                            w_comision * -1,
                            reg.margen * -1,
                            reg.porc_margen * -1,
                            f_pbase(reg.product_id) ,
                            reg.bono_comision * -1,
                            (w_comision+reg.bono_comision) * -1,
                            p_company_id ,
                            reg.devolucion * -1,
                            reg.doc_orig_dev,
                            reg.name);
                    ENd IF;
                      END LOOP;
                        --
                      --RETURN 0;
                      --	
                    END;
                    $BODY$;

                    ALTER FUNCTION public.f_comision_mayor_nc(integer, date, date)
                        OWNER TO odoo; """
        self.env.cr.execute(query)
        
        query = """insert into kcrea_funcion values 
        (nextval('nro_funcion'),4,2,2,'Generada la Function f_comision_mayor_nc en la Base de Datos'||' El dia: '|| to_char(CURRENT_TIMESTAMP, 'DD-MM-YYYY HH24:MI:SS'),'2024-09-06','2024-09-06');"""
        self.env.cr.execute(query)
#################################################################################
        query= """ DROP FUNCTION IF EXISTS public.f_comision_vendedores(integer, date, date);
                    CREATE OR REPLACE FUNCTION public.f_comision_vendedores(
                      p_company_id integer,
                      p_fecha_desde date,
                      p_fecha_hasta date)
                        RETURNS void
                        LANGUAGE 'plpgsql'
                        COST 100
                        VOLATILE PARALLEL UNSAFE
                    AS $BODY$
                    DECLARE
                      --
                      -- Declaracion  de Cursores
                      --
                      --
                        C_LINEAS_VENTAS CURSOR  FOR
                        SELECT o.company_id     ,
                            o.id             ,
                          o.name           ,
                          o.partner_id     ,
                            l.salesman_id    ,
                            l.product_id     ,
                            l.product_uom_qty,
                            l.price_subtotal ,
                            l.price_total ,
                              l.price_unit     ,
                          o.date_order     ,
                          case
                              when l.it_product_pricelist_id is null then o.pricelist_id
                          else
                          l.it_product_pricelist_id
                          end            precio_lista,
                          pat.id         marca,
                            o.margin       margen,
                          /*(o.margin/l.price_total)*100 porc_margen  ,*/
                          (o.margin/o.amount_untaxed)*100 porc_margen ,
                          case
                          when f_busca_devolucion(o.company_id,o.name,l.product_id) > 0 then 
                          0
                          else
                          f_bono_comision(o.company_id , o.id         , l.salesman_id,
                                              l.product_id , p_fecha_desde, p_fecha_hasta) 
                          end bono_comision,
                          f_busca_devolucion(o.company_id,o.name,l.product_id) devolucion,
                          f_busca_doc_orig_devolucion(o.company_id,o.name,l.product_id) doc_orig_dev							 
                          FROM sale_order     o,
                              sale_order_line  l, 
                          product_product pp,
                          product_template pt,
                          PRODUCT_TEMPLATE_ATTRIBUTE_LINE PTA,
                          product_attribute pat 
                        WHERE o.company_id = p_company_id 
                          AND o.company_id = l.company_id
                        AND o.id         = l.order_id
                        and l.product_id = pp.id
                        and pp.product_tmpl_id = pt.id 
                        AND pt.id =  pta.product_tmpl_id
                        and pta.attribute_id = pat.id
                        AND o.date_order >= p_fecha_desde 
                        AND o.date_order <= p_fecha_hasta
                        AND o.margin <> 0
                        AND l.price_total <> 0
                        AND l.product_uom_qty = l.qty_delivered;
                        --AND l.product_uom_qty = l.qty_invoiced;
                      --
                      reg            refcursor;
                      w_comision     numeric;
                      w_category_id  integer;
                      w_id           integer;
                      --
                    BEGIN
                      FOR reg IN C_LINEAS_VENTAS LOOP
                        --
                        -- Se realiza el calculo de la Comision
                        -- Retorna el monto de la comision
                          -- 
                        --w_category_id := f_busca_categoria( p_company_id => reg.company_id,
                        --                                   p_product_id => reg.product_id);
                        --
                        --w_category_id := f_get_category_id(reg.product_id);
                        --w_category_id := f_marca(1);
                        w_category_id := reg.marca;

                        w_comision := f_calcula_comision(
                                                          p_company_id    => reg.company_id  ,
                                                          p_precio_venta  => reg.price_unit  ,
                                                          p_monto_linea   => reg.price_total ,
                                                          p_marca_id      => w_category_id   ,
                                                          p_pricelist_id  => reg.precio_lista,
                                                        p_order_id      => reg.id
                                                        );

                          IF w_comision != 0 THEN
                            IF f_busca_devolucion(reg.company_id,reg.name,reg.product_id) > 0 THEN
                            w_comision = 0;
                          END IF;
                            select nextval('detalle_id_seq') into w_id;
                          INSERT INTO public.kdetalle_comisiones
                          ( id            ,	
                          create_uid     , 	
                          write_uid      , 
                          order_id       , 
                          vendedor_id    , 
                          cliente_id     ,	
                          pricelist_id   ,
                          marca_id       , 
                          fechadesde     , 
                          fechahasta     , 
                          date_order     ,
                          create_date    ,
                          write_date     ,
                          price_total    , 	   
                          porcentaje     , 		
                          porc_comision  ,
                          margen         ,
                          porc_margen    ,
                          precio_base    ,
                          bono_comision  ,
                          tot_bono_comision,
                          company_id,
                          devolucion,
                          doc_orig_dev,
                          name)
                          VALUES
                          (w_id           , 
                          1              ,	
                          1              , 
                          reg.id         ,
                          reg.salesman_id,
                          reg.partner_id,
                          reg.precio_lista,  
                          w_category_id  ,
                          p_fecha_desde  ,
                          p_fecha_hasta  ,
                            reg.date_order ,
                          current_date   ,
                          current_date   ,
                          reg.price_total ,	
                          (w_comision/reg.price_total)  * 100,  
                            w_comision,
                          reg.margen,
                          reg.porc_margen,
                          f_pbase(reg.product_id) ,
                          reg.bono_comision,
                          w_comision+reg.bono_comision,
                          p_company_id ,
                          reg.devolucion,
                          reg.doc_orig_dev,
                          reg.name);
                    ENd IF;
                      END LOOP;
                        --
                      --RETURN 0;
                      --	
                    END;
                    $BODY$;

                    ALTER FUNCTION public.f_comision_vendedores(integer, date, date)
                        OWNER TO odoo;
                    """
        self.env.cr.execute(query)
        
        query = """insert into kcrea_funcion values 
        (nextval('nro_funcion'),4,2,2,'Generada la Function f_comision_vendedores en la Base de Datos'||' El dia: '|| to_char(CURRENT_TIMESTAMP, 'DD-MM-YYYY HH24:MI:SS'),'2024-09-06','2024-09-06');"""
        self.env.cr.execute(query)
#################################################################################
        query= """ DROP FUNCTION IF EXISTS public.f_comision_vendedores_tienda(integer, date, date);
                    CREATE OR REPLACE FUNCTION public.f_comision_vendedores_tienda(
                      p_company_id integer,
                      p_fecha_desde date,
                      p_fecha_hasta date)
                        RETURNS void
                        LANGUAGE 'plpgsql'
                        COST 100
                        VOLATILE PARALLEL UNSAFE
                    AS $BODY$
                    DECLARE
                      --
                      -- Declaracion  de Cursores
                      --
                      --
                        C_LINEAS_VENTAS CURSOR  FOR
                      SELECT
                        hr.id                                                                        AS vendedor,
                        pc.id                                                                        AS tienda,
                        SUM(pol.price_unit * pol.qty)                                                AS monto_factura,
                        SUM(pol.price_unit * pol.qty * (pol.discount / 100))                         AS monto_descuento,
                        sum(price_subtotal)                                                          AS sub_total,
                        f_total_pos_vendedor(p_company_id,hr.id  ,p_fecha_desde,p_fecha_hasta)       AS total_factura,
                        --
                        f_comisiones_tienda_descuentos(po.company_id,
                                      pc.id,
                                      SUM(pol.price_unit*qty),
                                      SUM(pol.price_unit*qty * pol.discount / 100)) AS comision_descuento,
                        --
                        f_comisiones_tienda_ventas(po.company_id,pc.id,
                                    /*SUM(pol.price_unit*qty),*/
                                    SUM(pol.price_subtotal),
                                      SUM(pol.price_subtotal))                          AS comision_venta,
                        --
                        f_comisiones_tienda_descuentos(po.company_id,
                                      pc.id,
                                      SUM(pol.price_unit*qty),
                                      SUM(pol.price_unit*qty * pol.discount / 100)) +
                        --
                        f_comisiones_tienda_ventas(po.company_id,pc.id,
                                    SUM(pol.price_unit*qty),
                                      SUM(pol.price_subtotal))                          AS por_desc_mas_comision	,
                                    
                        --
                        --     TOATL A PAGAR SE LE RESTAN 100 AL TOTAL
                        CASE
                        WHEN 
                        (f_comisiones_tienda_descuentos(po.company_id,
                                      pc.id,
                                      SUM(pol.price_unit*qty),
                                      SUM(pol.price_unit*qty * pol.discount / 100)) +
                        --
                        f_comisiones_tienda_ventas(po.company_id,pc.id,
                                    SUM(pol.price_unit*qty),
                                      SUM(pol.price_subtotal))  ) - 100    <  0 THEN
                        0
                        ELSE
                        (f_comisiones_tienda_descuentos(po.company_id,
                                      pc.id,
                                      SUM(pol.price_unit*qty),
                                      SUM(pol.price_unit*qty * pol.discount / 100)) +
                        --
                        f_comisiones_tienda_ventas(po.company_id,pc.id,
                                    SUM(pol.price_unit*qty),
                                      SUM(pol.price_subtotal))  ) - 100 
                        END                                                         		    	 AS comision_a_pagar,
                        --
                        f_porc_tienda_ventas(po.company_id,pc.id,
                                    /*SUM(pol.price_unit*qty),*/
                                        SUM(pol.price_subtotal),
                                      SUM(pol.price_subtotal))                          AS porc_comision,
                        --
                        f_porc_tienda_descuentos(po.company_id,
                                      pc.id,
                                      SUM(pol.price_unit*qty),
                                      SUM(pol.price_unit*qty * pol.discount / 100))  AS porc_descuento,
                      to_char(po.date_order,'mmyyyy') periodo,
                      0 bono
                        --
                        FROM  pos_order       po,
                          pos_order_line  pol,
                              pos_session     ps,
                          pos_config      pc,
                            hr_employee     hr
                      WHERE po.company_id = p_company_id
                        AND po.session_id  = ps.id
                        AND  ps.config_id   = pc.id
                        AND  po.id          = pol.order_id
                        AND  po.employee_id = hr.id
                        AND  po.date_order >= p_fecha_desde 
                        AND  po.date_order <= p_fecha_hasta
                      GROUP BY  po.company_id,hr.id  ,pc.name , pc.id ,to_char(po.date_order,'mmyyyy');
                    --
                    reg            refcursor;
                    w_comision     numeric;
                    w_category_id  integer;
                    w_id           integer;
                    --
                    --
                    BEGIN
                      FOR reg IN C_LINEAS_VENTAS LOOP
                            select nextval('detalle_tienda_id_seq') into w_id;
                          INSERT INTO public.kdetalle_comisiones_tienda
                          ( id            ,	
                          company        ,
                          p_cia          ,
                          create_uid     , 	
                          write_uid      , 
                          company_id     ,
                          vendedor_id    ,
                          tienda_id      ,
                          fechadesde     ,
                          fechahasta     ,
                          create_date    ,
                          write_date     ,
                          monto_factura  ,
                          monto_descuento,
                          sub_total      ,
                          --total_factura  ,
                          comision_descuento,
                          comision_ventas,
                          comision_descuento_ventas,
                          -- comision_a_pagar,
                          porc_comision,
                          porc_descuento,
                          periodo,
                          bono)
                          VALUES
                          (w_id              , 
                          p_company_id       ,	
                          p_company_id       , 
                          2                  ,
                          2                  ,
                          p_company_id       ,
                          reg.vendedor       ,
                          reg.tienda         ,
                          p_fecha_desde      ,
                          p_fecha_hasta      ,
                          current_date       ,
                          current_date       ,
                          reg.monto_factura  ,
                          reg.monto_descuento,
                          reg.sub_total      ,
                          --reg.total_factura  ,
                          reg.comision_descuento,
                          reg.comision_venta   ,
                          reg.por_desc_mas_comision,
                          --reg.comision_a_pagar,
                          reg.porc_comision,
                          reg.porc_descuento,
                          reg.periodo,
                          reg.bono);
                      END LOOP;
                        --
                      --RETURN 0;
                      --	
                    END;
                    $BODY$;

                    ALTER FUNCTION public.f_comision_vendedores_tienda(integer, date, date)
                        OWNER TO odoo;
                      """
        self.env.cr.execute(query)
        
        query = """insert into kcrea_funcion values 
        (nextval('nro_funcion'),4,2,2,'Generada la Function f_comision_vendedores_tienda en la Base de Datos'||' El dia: '|| to_char(CURRENT_TIMESTAMP, 'DD-MM-YYYY HH24:MI:SS'),'2024-09-06','2024-09-06');"""
        self.env.cr.execute(query)
#################################################################################
        query= """ DROP FUNCTION IF EXISTS public.f_comision_vendedores_tienda_nc(integer, date, date);
                    CREATE OR REPLACE FUNCTION public.f_comision_vendedores_tienda_nc(
                      p_company_id integer,
                      p_fecha_desde date,
                      p_fecha_hasta date)
                        RETURNS void
                        LANGUAGE 'plpgsql'
                        COST 100
                        VOLATILE PARALLEL UNSAFE
                    AS $BODY$
                    DECLARE
                      --
                      -- Declaracion  de Cursores
                      --
                      --
                        C_LINEAS_VENTAS CURSOR  FOR
                        SELECT 
                        sol.salesman_id                                                  							       AS vendedor,
                      so.warehouse_id                                             								       AS tienda,
                        SUM(sol.price_unit * sol.product_uom_qty) * -1                                                     AS monto_factura,
                        SUM(sol.price_unit * sol.product_uom_qty * sol.discount / 100) * -1                                AS monto_descuento,
                        SUM(sol.price_subtotal)     * -1                                                                   AS sub_total,
                        SUM(sol.price_total)  * -1                                                                             AS total_factura,
                        f_comisiones_tienda_descuentos(so.company_id,
                                      pc.id,
                                      SUM(sol.price_total),
                                      SUM(sol.price_unit * sol.product_uom_qty * sol.discount / 100)) * -1 AS comision_descuento,
                                      
                      f_comisiones_tienda_ventas(so.company_id,
                                    pc.id,
                                    SUM(sol.price_total),
                                      SUM(sol.price_subtotal))                                           * -1 AS comision_venta,
                                    
                      f_comisiones_tienda_descuentos(so.company_id,
                                      pc.id,
                                      SUM(sol.price_total),
                                      SUM(sol.price_unit * sol.product_uom_qty * sol.discount / 100)) * -1  +
                                      
                      f_comisiones_tienda_ventas(so.company_id,
                                    pc.id,
                                    SUM(sol.price_total),
                                      SUM(sol.price_subtotal)) * -1                                           AS por_desc_mas_comision	
                    FROM
                        sale_order so,
                      sale_order_line sol,
                      account_move   ac
                    where so.company_id = p_company_id
                      and so.company_id = sol.company_id
                      and so.company_id = ac.company_id
                      and sol.order_id  = so.id
                      and so.name   = ac.invoice_origin
                      and ac.reversed_entry_id is not null
                      --and so.id = 68
                      and ac.date   between p_fecha_desde and p_fecha_hasta
                    GROUP BY so.company_id,sol.salesman_id  ,so.warehouse_id;
                    --
                    reg            refcursor;
                    w_comision     numeric;
                    w_category_id  integer;
                    w_id           integer;
                    --
                    --
                    BEGIN
                      FOR reg IN C_LINEAS_VENTAS LOOP
                            select nextval('detalle_tienda_id_seq') into w_id;
                          INSERT INTO public.kdetalle_comisiones_tienda
                          ( id            ,	
                          company        ,
                          p_cia          ,
                          create_uid     , 	
                          write_uid      , 
                          company_id     ,
                          /*order_id       , */
                          vendedor_id    , 
                          tienda_id      ,
                          /*name           ,*/
                          fechadesde     ,
                          fechahasta     ,
                          /*date_order     ,*/
                          create_date    ,
                          write_date     ,
                          monto_factura  ,
                          monto_descuento,
                          sub_total      ,
                          total_factura  ,
                          comision_descuento,
                          comision_ventas,
                          comision_descuento_ventas)
                          VALUES
                          (w_id              , 
                          p_company_id       ,	
                          p_company_id       , 
                          2                  ,
                          2                  ,
                          p_company_id       ,
                          /*reg.pedido         ,*/
                          reg.vendedor       ,
                          reg.tienda         ,
                          /*reg.name           ,*/
                          p_fecha_desde      ,
                          p_fecha_hasta      ,
                          /*reg.fecha         ,*/
                          current_date       ,
                          current_date       ,
                          reg.monto_factura  ,
                          reg.monto_descuento,
                          reg.sub_total      ,
                          reg.total_factura  ,
                          reg.comision_descuento,
                          reg.comision_venta   ,
                          reg.por_desc_mas_comision);
                      END LOOP;
                        --
                      --RETURN 0;
                      --	
                    END;
                    $BODY$;

                    ALTER FUNCTION public.f_comision_vendedores_tienda_nc(integer, date, date)
                        OWNER TO odoo;
                    """
        self.env.cr.execute(query)
        
        query = """insert into kcrea_funcion values 
        (nextval('nro_funcion'),4,2,2,'Generada la Function f_comision_vendedores_tienda_nc en la Base de Datos'||' El dia: '|| to_char(CURRENT_TIMESTAMP, 'DD-MM-YYYY HH24:MI:SS'),'2024-09-06','2024-09-06');"""
        self.env.cr.execute(query)
#################################################################################
        query= """ DROP FUNCTION IF EXISTS public.f_comisiones_tienda_descuentos(integer, integer, double precision, double precision);
                    CREATE OR REPLACE FUNCTION public.f_comisiones_tienda_descuentos(
                      p_company integer,
                      p_tienda integer,
                      p_monto_comi double precision,
                      p_monto_desc double precision)
                        RETURNS double precision
                        LANGUAGE 'plpgsql'
                        COST 100
                        VOLATILE PARALLEL UNSAFE
                    AS $BODY$
                    --
                    DECLARE
                    w_monto numeric := 0;
                    reg           record;
                    --
                    -- Declaracion  de Cursores
                    --
                    --
                    BEGIN
                    FOR reg IN (SELECT porc_descuento,
                                ind_porc_desc
                            FROM kporcentaje_comisiones
                                WHERE  company_id = p_company
                            AND  tienda_id  = p_tienda
                                  AND  p_monto_comi between monto_desde and monto_hasta)
                        
                      LOOP
                        IF REG.ind_porc_desc = 'S' THEN
                            w_monto := p_monto_desc * (reg.porc_descuento/100);
                      ELSE
                            w_monto := 0;
                      END IF;
                      END LOOP;
                      RETURN w_monto;
                    END;
                    $BODY$;

                    ALTER FUNCTION public.f_comisiones_tienda_descuentos(integer, integer, double precision, double precision)
                        OWNER TO odoo;
                    """
        self.env.cr.execute(query)
        
        query = """insert into kcrea_funcion values 
        (nextval('nro_funcion'),4,2,2,'Generada la Function f_comisiones_tienda_descuentos en la Base de Datos'||' El dia: '|| to_char(CURRENT_TIMESTAMP, 'DD-MM-YYYY HH24:MI:SS'),'2024-09-06','2024-09-06');"""
        self.env.cr.execute(query)
#################################################################################
        query= """ DROP FUNCTION IF EXISTS public.f_comisiones_tienda_ventas(integer, integer, double precision, double precision);
                    CREATE OR REPLACE FUNCTION public.f_comisiones_tienda_ventas(
                      p_company_id integer,
                      p_tienda_id integer,
                      p_monto_total double precision,
                      p_monto_sub_total double precision)
                        RETURNS double precision
                        LANGUAGE 'plpgsql'
                        COST 100
                        VOLATILE PARALLEL UNSAFE
                    AS $BODY$
                    --
                    DECLARE
                    w_monto numeric := 0;
                    reg           record;
                    --
                    -- Declaracion  de Cursores
                    --
                    --
                    BEGIN
                    FOR reg IN (SELECT porcentaje 
                            FROM kporcentaje_comisiones
                                WHERE  p_company_id = p_company_id 
                            AND  tienda_id    = p_tienda_id
                            AND  p_monto_sub_total between monto_desde and monto_hasta)
                                  --AND  p_monto_total between monto_desde and monto_hasta) 
                        
                      LOOP
                            w_monto :=  p_monto_sub_total * (reg.porcentaje/100);
                      END LOOP;
                      RETURN w_monto;
                    END;
                    $BODY$;

                    ALTER FUNCTION public.f_comisiones_tienda_ventas(integer, integer, double precision, double precision)
                        OWNER TO odoo; """
        self.env.cr.execute(query)
        
        query = """insert into kcrea_funcion values 
        (nextval('nro_funcion'),4,2,2,'Generada la Function f_comisiones_tienda_ventas en la Base de Datos'||' El dia: '|| to_char(CURRENT_TIMESTAMP, 'DD-MM-YYYY HH24:MI:SS'),'2024-09-06','2024-09-06');"""
        self.env.cr.execute(query)
#################################################################################
        query= """ DROP FUNCTION IF EXISTS public.f_insert_bono_comision(integer);
                    CREATE OR REPLACE FUNCTION public.f_insert_bono_comision(
                      p_company_id integer)
                        RETURNS double precision
                        LANGUAGE 'plpgsql'
                        COST 100
                        VOLATILE PARALLEL UNSAFE
                    AS $BODY$
                    --
                    DECLARE
                    reg           record;
                    --
                    -- Declaracion  de Cursores
                    --
                    --
                    BEGIN
                    --
                    FOR reg IN 
                        ( select distinct ka.company_id  cia,
                                          CAST(sw.code AS integer) codigo,
                                    ka.descripcion descripcion, 
                                    ka.fechadesde  fechadesde,
                                    ka.fechahasta  fechahasta
                                from kbono_arinbo ka, stock_warehouse sw
                                where ka.company_id = p_company_id
                                and ka.company_id = sw.company_id
                                  and ka.warehouse_id = sw.id 
                                LIMIT 1)
                      LOOP
                          insert into public.kbono_comisiones
                          (id,
                        company_id, 
                        codigo_bono_id,
                        create_uid,
                        write_uid,
                        descripcion,
                        fechadesde,
                        fechahasta,
                        create_date,
                        write_date)
                    VALUES
                            (nextval('SECUENCIA_BONO_COMISIONES'),
                        reg.cia, 
                        CAST(nextval('SECUENCIA_CODIGO_BONO')||'0'||reg.codigo AS integer),
                        2,
                        2,
                        reg.descripcion,
                        reg.fechadesde,
                        reg.fechahasta,
                        CURRENT_DATE ,
                        CURRENT_DATE );
                      END LOOP;
                    RETURN null;
                    --
                    -- INSERTA EN DETALLE X ARTICULOS
                    --
                    END;
                    $BODY$;

                    ALTER FUNCTION public.f_insert_bono_comision(integer)
                        OWNER TO odoo;
                    """
        self.env.cr.execute(query)
        
        query = """insert into kcrea_funcion values 
        (nextval('nro_funcion'),4,2,2,'Generada la Function f_insert_bono_comision en la Base de Datos'||' El dia: '|| to_char(CURRENT_TIMESTAMP, 'DD-MM-YYYY HH24:MI:SS'),'2024-09-06','2024-09-06');"""
        self.env.cr.execute(query)
#################################################################################
        query= """ DROP FUNCTION IF EXISTS public.f_insert_bono_detalle(integer);
                    CREATE OR REPLACE FUNCTION public.f_insert_bono_detalle(
                      p_company_id integer)
                        RETURNS double precision
                        LANGUAGE 'plpgsql'
                        COST 100
                        VOLATILE PARALLEL UNSAFE
                    AS $BODY$
                    --
                    DECLARE
                    reg           record;
                    --
                    -- Declaracion  de Cursores
                    --
                    --
                    BEGIN
                    --
                    --
                    -- INSERTA EN DETALLE X ARTICULOS
                    --
                    FOR reg IN 
                        ( select kc.id ,
                              kc.company_id cia,
                                ka.warehouse_id almacen, 
                              ka.product_id   producto,
                              2,
                              2,
                              current_date, 
                              current_date, 
                              ka.monto_bono, 
                              ka.meta,
                              ka.monto_meta
                        from  kbono_comisiones kc, kbono_arinbo ka
                      where kc.company_id = p_company_id
                      and kc.company_id = ka.company_id)
                      LOOP
                          insert into public.kbono_detalle
                          (id,
                        company_id, 
                        codigo_bono_id,
                        warehouse_id,
                        product_id,
                        create_uid,
                        write_uid,
                        create_date,
                        write_date,
                          monto_bono,
                          meta,
                          monto_meta)
                    VALUES
                            (nextval('SECUENCIA_BONO_DETALLE'),
                        reg.cia, 
                        reg.id,
                        reg.almacen,
                        reg.producto,
                        2,
                        2,
                        CURRENT_DATE ,
                        CURRENT_DATE,
                        reg.monto_bono,
                        reg.meta,
                        reg.monto_meta);
                      END LOOP;
                      RETURN null;
                    --	 
                    END;
                    $BODY$;

                    ALTER FUNCTION public.f_insert_bono_detalle(integer)
                        OWNER TO odoo;
                    """
        self.env.cr.execute(query)
        
        query = """insert into kcrea_funcion values 
        (nextval('nro_funcion'),4,2,2,'Generada la Function f_insert_bono_detalle en la Base de Datos'||' El dia: '|| to_char(CURRENT_DATE, 'DD-MM-YYYY HH24:MI:SS'),'2024-09-06','2024-09-06');"""
        self.env.cr.execute(query)
#################################################################################
        query= """ DROP FUNCTION IF EXISTS public.f_porc_tienda_descuentos(integer, integer, double precision, double precision);
                    CREATE OR REPLACE FUNCTION public.f_porc_tienda_descuentos(
                      p_company integer,
                      p_tienda integer,
                      p_monto_comi double precision,
                      p_monto_desc double precision)
                        RETURNS double precision
                        LANGUAGE 'plpgsql'
                        COST 100
                        VOLATILE PARALLEL UNSAFE
                    AS $BODY$
                    --
                    DECLARE
                    w_monto numeric := 0;
                    reg           record;
                    --
                    -- Declaracion  de Cursores
                    --
                    --
                    BEGIN
                    FOR reg IN (SELECT porc_descuento,
                                ind_porc_desc
                            FROM kporcentaje_comisiones
                                WHERE  company_id = p_company
                            AND  tienda_id  = p_tienda
                                  AND  p_monto_comi between monto_desde and monto_hasta)
                        
                      LOOP
                        IF REG.ind_porc_desc = 'S' THEN
                            w_monto := reg.porc_descuento;
                      ELSE
                            w_monto := 0;
                      END IF;
                      END LOOP;
                      RETURN w_monto;
                    END;
                    $BODY$;

                    ALTER FUNCTION public.f_porc_tienda_descuentos(integer, integer, double precision, double precision)
                        OWNER TO odoo;
                    """
        self.env.cr.execute(query)
        
        query = """insert into kcrea_funcion values 
        (nextval('nro_funcion'),4,2,2,'Generada la Function f_porc_tienda_descuentos en la Base de Datos'||' El dia: '|| to_char(CURRENT_TIMESTAMP, 'DD-MM-YYYY HH24:MI:SS'),'2024-09-06','2024-09-06');"""
        self.env.cr.execute(query)
#################################################################################
        query= """ DROP FUNCTION IF EXISTS public.f_porc_tienda_ventas(integer, integer, double precision, double precision);
                    CREATE OR REPLACE FUNCTION public.f_porc_tienda_ventas(
                      p_company_id integer,
                      p_tienda_id integer,
                      p_monto_total double precision,
                      p_monto_sub_total double precision)
                        RETURNS double precision
                        LANGUAGE 'plpgsql'
                        COST 100
                        VOLATILE PARALLEL UNSAFE
                    AS $BODY$
                    --
                    DECLARE
                    w_monto numeric := 0;
                    reg           record;
                    --
                    -- Declaracion  de Cursores
                    --
                    --
                    BEGIN
                    FOR reg IN (SELECT porcentaje 
                            FROM kporcentaje_comisiones
                                WHERE  p_company_id = p_company_id 
                            AND  tienda_id    = p_tienda_id
                                  AND  p_monto_total between monto_desde and monto_hasta) 
                        
                      LOOP
                            w_monto :=  reg.porcentaje;
                      END LOOP;
                      RETURN w_monto;
                    END;
                    $BODY$;

                    ALTER FUNCTION public.f_porc_tienda_ventas(integer, integer, double precision, double precision)
                        OWNER TO odoo;
                    """
        self.env.cr.execute(query)
        
        query = """insert into kcrea_funcion values 
        (nextval('nro_funcion'),4,2,2,'Generada la Function f_porc_tienda_ventas en la Base de Datos'||' El dia: '|| to_char(CURRENT_TIMESTAMP, 'DD-MM-YYYY HH24:MI:SS'),'2024-09-06','2024-09-06');"""
        self.env.cr.execute(query)
#################################################################################
        query= """ DROP FUNCTION IF EXISTS public.f_promedio_ventas(integer, character varying);
                    CREATE OR REPLACE FUNCTION public.f_promedio_ventas(
                      p_product_id integer,
                      p_state character varying)
                        RETURNS numeric
                        LANGUAGE 'plpgsql'
                        COST 100
                        VOLATILE PARALLEL UNSAFE
                    AS $BODY$
                    --
                    DECLARE
                    w_promedio integer := 0;
                    reg                record;
                    --
                    -- Declaracion  de Cursores
                    --
                    --
                    BEGIN
                    FOR reg IN (SELECT SUM(price_total) / SUM(sol.product_uom_qty) AS promedio
                                FROM sale_order_line sol,
                                      sale_order so, 
                                      product_template p
                                WHERE sol.order_id = so.id
                                  AND p.id         = sol.product_id 
                                  AND P.ID         = p_product_id
                                  AND so.state     = p_state
                                  AND so.date_order >= to_date('0101'||EXTRACT(YEAR FROM NOW()), 'DDMMYYYY')
                                  AND so.date_order <= NOW()
                        
                        )
                        
                      LOOP
                            w_promedio := reg.promedio;
                      END LOOP;
                      RETURN w_promedio;
                    END;
                    $BODY$;

                    ALTER FUNCTION public.f_promedio_ventas(integer, character varying)
                        OWNER TO odoo;
                    """
        self.env.cr.execute(query)
        
        query = """insert into kcrea_funcion values 
        (nextval('nro_funcion'),4,2,2,'Generada la Function f_promedio_ventas en la Base de Datos'||' El dia: '|| to_char(CURRENT_TIMESTAMP, 'DD-MM-YYYY HH24:MI:SS'),'2024-09-06','2024-09-06');"""
        self.env.cr.execute(query)
#################################################################################
        query= """  DROP FUNCTION IF EXISTS public.f_total_pos_vendedor(integer, integer, date, date);
                    CREATE OR REPLACE FUNCTION public.f_total_pos_vendedor(
                      p_company_id integer,
                      p_vendedor_id integer,
                      fechadesde date,
                      fechahasta date)
                        RETURNS numeric
                        LANGUAGE 'plpgsql'
                        COST 100
                        VOLATILE PARALLEL UNSAFE
                    AS $BODY$
                    --
                    DECLARE
                    w_total       integer;
                    reg           record;
                    --
                    -- Declaracion  de Cursores
                    --
                    --
                    BEGIN
                    FOR reg IN (select sum(amount_total) total
                                  from pos_order po,   hr_employee hr
                                where po.company_id = p_company_id
                            AND  po.employee_id     = p_vendedor_id
                                  AND  po.employee_id     = hr.id
                                  AND  date_order between fechadesde and fechahasta) 
                        
                      LOOP
                            w_total := reg.total;
                      END LOOP;
                      RETURN w_total;
                    END;
                    $BODY$;

                    ALTER FUNCTION public.f_total_pos_vendedor(integer, integer, date, date)
                        OWNER TO odoo;
                    """
        self.env.cr.execute(query)
        
        query = """insert into kcrea_funcion values 
        (nextval('nro_funcion'),4,2,2,'Generada la Function f_total_pos_vendedor en la Base de Datos'||' El dia: '|| to_char(CURRENT_TIMESTAMP, 'DD-MM-YYYY HH24:MI:SS'),'2024-09-06','2024-09-06');"""
        self.env.cr.execute(query)


