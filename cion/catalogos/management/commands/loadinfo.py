from django.core.management.base import BaseCommand
from catalogos.models import areas, Servicios,Estado,Municipio,tipoServicioAgua
from django.core.management import call_command  # Correct import for call_command
from usuarios.models import CustomUser
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Carga datos iniciales en varios modelos'

    def handle(self, *args, **options):
        self.stdout.write("Iniciando la carga de datos...")
        self.cargar_areas()
        self.cargar_servicios()
        self.cargar_estados()
        self.cargar_municipios_tlaxcala()
        self.cargar_tipos_servicio_agua()

        self.stdout.write("Carga de datos completada.")
        self.stdout.write("Iniciando la importación de códigos postales...")
        self.importar_codigos_postales()
        self.crear_usuario_admin()

    def cargar_tipos_servicio_agua(self):
        todos_los_municipios = Municipio.objects.all()
        for municipio in todos_los_municipios:
            tipo_servicio_comision, created_comision = tipoServicioAgua.objects.get_or_create(
                tipoServicio="COMISIÓN",
                municipio=municipio
            )
            if created_comision:
                self.stdout.write(f'Tipo de servicio agua "COMISIÓN" creado para el municipio {municipio.nombre}')

            tipo_servicio_municipal, created_municipal = tipoServicioAgua.objects.get_or_create(
                tipoServicio="MUNICIPAL",
                municipio=municipio
            )
            if created_municipal:
                self.stdout.write(f'Tipo de servicio agua "MUNICIPAL" creado para el municipio {municipio.nombre}')

    def cargar_municipios_tlaxcala(self):
        estado_tlaxcala = Estado.objects.filter(nombre="Tlaxcala").first()
        if not estado_tlaxcala:
            self.stdout.write("Estado de Tlaxcala no encontrado, abortando carga de municipios.")
            return
        
        datos_municipios = [
            (1, 'Amaxac de Guerrero'),
            (2, 'Apetatitlán de Antonio Carvajal'),
            (3, 'Atlangatepec'),
            (4, 'Altzayanca'),
            (5, 'Apizaco'),
            (6, 'Calpulalpan'),
            (7, 'El Carmen Tequexquitla'),
            (8, 'Cuapiaxtla'),
            (9, 'Cuaxomulco'),
            (10, 'Chiautempan'),
            (11, 'Muñoz de Domingo Arenas'),
            (12, 'Españita'),
            (13, 'Huamantla'),
            (14, 'Hueyotlipan'),
            (15, 'Ixtacuixtla de Mariano Matamoros'),
            (16, 'Ixtenco'),
            (17, 'Mazatecochco de José María Morelos'),
            (18, 'Contla de Juan Cuamatzi'),
            (19, 'Tepetitla de Lardizábal'),
            (20, 'Sanctórum de Lázaro Cárdenas'),
            (21, 'Nanacamilpa de Mariano Arista'),
            (22, 'Acamanala de Miguel Hidalgo'),
            (23, 'Nativitas'),
            (24, 'Panotla'),
            (25, 'San Pablo del Monte'),
            (26, 'Santa Cruz Tlaxcala'),
            (27, 'Tenancingo'),
            (28, 'Teolocholco'),
            (29, 'Tepetitla'),
            (30, 'Terrenate'),
            (31, 'Tetla de la Solidaridad'),
            (32, 'Tetlatlahuca'),
            (33, 'Tlaxcala'),
            (34, 'Tlaxco'),
            (35, 'Tocatlán'),
            (36, 'Totolac'),
            (37, 'Ziltlaltépec de Trinidad Sánchez Santos'),
            (38, 'Tzompantepec'),
            (39, 'Xaloztoc'),
            (40, 'Xaltocan'),
            (41, 'Papalotla de Xicohténcatl'),
            (42, 'Xicohtzinco'),
            (43, 'Yauhquemehcan'),
            (44, 'Zacatelco'),
            (45, 'Benito Juárez'),
            (46, 'Emiliano Zapata'),
            (47, 'Lázaro Cárdenas'),
            (48, 'La Magdalena Tlaltelulco'),
            (49, 'San Damián Texóloc'),
            (50, 'San Francisco Tetlanohcan'),
            (51, 'San Jerónimo Zacualpan'),
            (52, 'San José Teacalco'),
            (53, 'San Juan Huactzinco'),
            (54, 'San Lorenzo Axocomanitla'),
            (55, 'San Lucas Tecopilco'),
            (56, 'Santa Ana Nopalucan'),
            (57, 'Santa Apolonia Teacalco'),
            (58, 'Santa Catarina Ayometla'),
            (59, 'Santa Cruz Quilehtla'),
            (60, 'Santa Isabel Xiloxoxtla'),
        ]


        for numero, nombre in datos_municipios:
            municipio, created = Municipio.objects.get_or_create(
                numero_municipio=numero, 
                nombre=nombre, 
                estado=estado_tlaxcala
            )
            if created:
                self.stdout.write(f'Municipio creado: {nombre}')
            else:
                self.stdout.write(f'Municipio ya existía: {nombre}')
    def cargar_estados(self):
        datos_estados = [
            (1, 'Aguascalientes'),
            (2, 'Baja California'),
            (3, 'Baja California Sur'),
            (4, 'Campeche'),
            (5, 'Chiapas'),
            (6, 'Chihuahua'),
            (7, 'Ciudad de México'),
            (8, 'Coahuila'),
            (9, 'Colima'),
            (10, 'Durango'),
            (11, 'Estado de México'),
            (12, 'Guanajuato'),
            (13, 'Guerrero'),
            (14, 'Hidalgo'),
            (15, 'Jalisco'),
            (16, 'Michoacán'),
            (17, 'Morelos'),
            (18, 'Nayarit'),
            (19, 'Nuevo León'),
            (20, 'Oaxaca'),
            (21, 'Puebla'),
            (22, 'Querétaro'),
            (23, 'Quintana Roo'),
            (24, 'San Luis Potosí'),
            (25, 'Sinaloa'),
            (26, 'Sonora'),
            (27, 'Tabasco'),
            (28, 'Tamaulipas'),
            (29, 'Tlaxcala'),
            (30, 'Veracruz'),
            (31, 'Yucatán'),
            (32, 'Zacatecas'),
        ]
        for numero, nombre in datos_estados:
            estado, created = Estado.objects.get_or_create(numero_estado=numero, nombre=nombre)
            if created:
                self.stdout.write(f'Estado creado: {nombre}')
            else:
                self.stdout.write(f'Estado ya existía: {nombre}')

    def cargar_areas(self):
        nombres_de_areas = ['Area 1', 'Area 2']
        for nombre in nombres_de_areas:
            area, created = areas.objects.get_or_create(Area=nombre)
            if created:
                self.stdout.write(f'Área creada: {nombre}')
            else:
                self.stdout.write(f'Área ya existía: {nombre}')

    def cargar_servicios(self):
        datos_servicios = [
            ('0', 'INGRESOS DERIVADOS DE FINANCIAMIENTOS'),
            ('0.0', 'INGRESOS DERIVADOS DE FINANCIAMIENTOS'),
            ('0.1', 'ENDEUDAMIENTO INTERNO'),
            ('0.2', 'ENDEUDAMIENTO EXTERNO'),
            ('0.3', 'FINANCIAMIENTO INTERNO'),
            ('1', 'IMPUESTOS'),
            ('1.1', 'IMPUESTOS SOBRE LOS INGRESOS'),
            ('1.1.1', 'IMPUESTO S/DIVERS. Y ESPECTÁCULOS PÚB.'),
            ('1.2', 'IMPUESTOS SOBRE EL PATRIMONIO'),
            ('1.2.1', 'IMPUESTO PREDIAL'),
            ('1.2.1.1', 'URBANO'),
            ('1.2.1.2', 'RÚSTICO'),
            ('1.2.2', 'TRANSMISIÓN DE BIENES INMUEBLES'),
            ('1.2.2.1', 'TRANSMISIÓN DE BIENES INMUEBLES'),
            ('1.3', 'IMPUESTOS S/LA PROD. E/CONS.Y L/TRANS.'),
            ('1.3.1', 'IMPUESTO S/LA PROD. E/CONS.Y L/TRANS.'),
            ('1.4', 'IMPUESTOS AL COMERCIO EXTERIOR'),
            ('1.4.1', 'IMPUESTOS AL COMERCIO EXTERIOR'),
            ('1.5', 'IMPUESTOS SOBRE NÓMINAS Y ASIMILABLES'),
            ('1.5.1', 'IMPUESTO SOBRE NÓMINAS Y ASIMILABLES'),
            ('1.6', 'IMPUESTOS ECOLÓGICOS'),
            ('1.6.1', 'IMPUESTOS ECOLÓGICOS'),
            ('1.7', 'ACCESORIOS DE IMPUESTOS'),
            ('1.7.1', 'RECARGOS'),
            ('1.7.1.1', 'RECARGOS PREDIAL'),
            ('1.7.1.2', 'RECARGOS OTROS'),
            ('1.7.2', 'MULTAS'),
            ('1.7.2.1', 'MULTAS PREDIAL'),
            ('1.7.2.2', 'MULTAS OTROS'),
            ('1.7.3', 'ACTUALIZACIÓN'),
            ('1.7.3.1', 'ACTUALIZACIÓN PREDIAL'),
            ('1.7.3.2', 'ACTUALIZACIÓN OTROS'),
            ('1.8', 'OTROS IMPUESTOS'),
            ('1.8.1', 'OTROS IMPUESTOS'),
            ('1.9', 'IMP. NO COMPRENDIDOS EN LA LEY DE ING. VIGENTE CAUS. EN EJER. FISC. ANT. PEND.'),
            ('1.9.1', 'IMPUESTOS NO COMP. E/LA LEY D/INGRESOS'),
            ('2', 'CUOTAS Y APORT. DE SEGURIDAD SOCIAL'),
            ('2.1', 'APORTACIONES PARA FONDOS DE VIVIENDA'),
            ('2.1.1', 'APORTACIONES PARA FONDOS DE VIVIENDA'),
            ('2.2', 'CUOTAS PARA LA SEGURIDAD SOCIAL'),
            ('2.2.1', 'CUOTAS PARA EL SEGURO SOCIAL'),
            ('2.3', 'CUOTAS DE AHORRO PARA EL RETIRO'),
            ('2.3.1', 'CUOTAS DE AHORRO PARA EL RETIRO'),
            ('2.4', 'OTRAS CUOTAS Y APORT. P/LA SEG. SOCIAL'),
            ('2.4.1', 'OTRAS CUOTAS Y APORT. P/LA SEG. SOCIAL'),
            ('2.5', 'ACCESORIOS DE CUOTAS Y APORTACIONES PARA LA SEGURIDAD SOCIAL'),
            ('2.5.1', 'RECARGOS'),
            ('2.5.1.1', 'RECARGOS'),
            ('2.5.2', 'MULTAS'),
            ('2.5.2.1', 'MULTAS'),
            ('2.5.3', 'ACTUALIZACIÓN'),
            ('2.5.3.1', 'ACTUALIZACIÓN'),
            ('3', 'CONTRIBUCIONES DE MEJORAS'),
            ('3.1', 'CONTRIBUCIONES DE MEJORAS POR OBRAS PÚBLICAS'),
            ('3.1.1', 'CONTRIBUCIÓN DE MEJORAS POR OBRAS PUB.'),
            ('3.1.1.1', 'APORTACIÓN DE BENEFICIARIOS'),
            ('3.9', 'CON. DE MEJ. NO COMP. EN LA LEY DE ING. VIGENTE, CAUS. EN EJER. FISC. ANT. PEND. DE LIO. O PAGO'),
            ('3.9.1', 'CONTRIB. MEJ. NO COMP. LEY INGRESOS'),
            ('4', 'DERECHOS'),
            ('4.1', 'DER. USO, GOCE, APROV. O EXP. BIENES DE D.P.'),
            ('4.1.1', 'DER. USO, GOCE, APROV. O EXP. BIENES DE D.P.'),
            ('4.1.3', 'DERECHOS POR PRESTACIÓN DE SERVICIOS'),
            ('4.3.1.1', 'AVALÚO DE PREDIOS URBANO'),
            ('4.3.1.2', 'AVALÚO DE PREDIOS RÚSTICO'),
            ('4.3.1.3', 'MANIFESTACIONES CATASTRALES'),
            ('4.3.1.4', 'AVISOS NOTARIALES'),
            ('4.3.2.1', 'ALINEAMIENTO DE INMUEBLES'),
            ('4.3.2.2', 'LICENC. CONST. OBRA. NVA. AMP. REV. MEM. CÁLC.'),
            ('4.3.2.4', 'LICENCIAS P/DIVIDIR, FUSIONAR Y LOTIF.'),
            ('4.3.2.5', 'DICTAMEN DE USO DE SUELO'),
            ('4.3.2.6', 'SERVICIO DE VIG. INSP. Y CTROL DE LEYES'),
            ('4.3.2.7', 'CONSTANCIA DE SERVICIOS PÚBLICOS'),
            ('4.3.2.8', 'DESLINDE DE TERRENOS Y RECTIFICACIÓN DE MEDIDAS'),
            ('4.3.2.9', 'REGULAR. LAS OBRAS CONST. SIN LICENCIA'),
            ('4.3.2.A', 'INSIGNC. D/NUM. OFICIAL BIENES INMUEB.'),
            ('4.3.2.B', 'OBSTRUCCIÓN DE LUG. PÚB. CON MATER.'),
            ('4.3.2.C', 'PERMISO OBST. VÍAS Y LUG. PÚB. MAT.'),
            ('4.3.2.D', 'PERMISO P/EL EXT. MAT. PÉT. MIN. O SUST.'),
            ('4.3.2.E', 'INSCRIPCIÓN AL PADRÓN DE CONTRATISTAS'),
            ('4.3.2.F', 'BASES DE CONCURSOS Y LICITACIONES'),
            ('4.3.3', 'SERVICIO PRESTADO EN EL RASTRO MUNICIPAL'),
            ('4.3.3.1', 'RASTRO MUNICIPAL'),
            ('4.3.3.A', 'EXPEDICIÓN DE CERTIF. Y CONST. EN GRAL.'),
            ('4.3.4', 'EXPEDICIÓN DE CERTIF. Y CONST.'),
            ('4.3.4.1', 'BÚSQUEDA Y COPIA DE DOCUMENTOS'),
            ('4.3.4.2', 'EXPEDICIÓN DE CERTIFICACIONES OFICIALES'),
            ('4.3.4.3', 'EXPED. CONST. D/POSESIÓN D/PREDIOS'),
            ('4.3.4.4', 'EXPEDICIÓN DE CONSTANCIAS'),
            ('4.3.4.5', 'EXPEDICIÓN DE OTRAS CONSTANCIAS'),
            ('4.3.4.6', 'CANJE DEL FORMATO DE LICENCIA DE FUNC.'),
            ('4.3.4.7', 'REPOSIC. P/PERD./DEFORMATO D/LIC.'),
            ('4.3.5', 'REGISTRO DEL ESTADO CIVIL D/LAS PERSONAS'),
            ('4.3.5.1', 'ACTAS DE NACIMIENTO'),
            ('4.3.5.2', 'ACTAS DE MATRIMONIO'),
            ('4.3.5.3', 'ACTAS DE DIVORCIO'),
            ('4.3.5.4', 'ACTAS DE DEFUNCIÓN'),
            ('4.3.5.5', 'CELEBRACIÓN DE MATRIMONIOS'),
            ('4.3.5.6', 'DISPENSA D/LA PUB. P/CONTRAER MATRIM.'),
            ('4.3.5.7', 'EXPEDICIÓN DE COPIAS CERTIFICADAS'),
            ('4.3.5.8', 'ANOTACIÓN MARG. E/TAB. D/REGISTRO CIVIL'),
            ('4.3.5.9', 'EXPEDICIÓN DE CONSTANCIAS'),
            ('4.3.5.A', 'EXPEDIC. D/COP SEMPL. D/ACTOS REGIST.'),
            ('4.3.5.B', 'ORDEN DE INHUMACIÓN'),
            ('4.3.6', 'SERVICIO DE LIMPIA'),
            ('4.3.6.1', 'TRANSP. Y DISP.FINAL D/DES.SÓL. INDUST.'),
            ('4.3.6.2', 'TRANSP.Y DISP.FINAL DES.SÓL. COM.Y SERV.'),
            ('4.3.6.3', 'TRANSP. Y DISP.FINAL DES.SÓL. ORG.'),
            ('4.3.6.4', 'TRANSP. Y DISP.FINAL DES.SÓL E/LOT. BALD.'),
            ('4.3.7', 'USO DE LA VÍA Y LUGARES PÚBLICOS'),
            ('4.3.7.1', 'USO DE LA VÍA Y LUGARES PÚBLICOS'),
            ('4.3.7.2', 'SERVICIO DE PANTALLONES'),
            ('4.3.8', 'SERVICIOS Y AUTORIZACIONES DIVERSAS'),
            ('4.3.8.1', 'LICENCIAS DE FUNC. P/VENTA D/BEB. ALCOH.'),
            ('4.3.8.2', 'LICENCIAS DE FUNCIONAMIENTO'),
            ('4.3.8.3', 'EMPADRONAMIENTO MUNICIPAL'),
            ('4.3.9.1', 'EXPED. O REFEREN. LIC. P/L COL. ANUNC. PUB.'),
            ('4.3.9.2', 'ANUNCIOS ADOSADOS'),
            ('4.3.9.3', 'ANUNCIOS PINTADOS Y/O MURALES'),
            ('4.3.9.4', 'ESTRUCTURALES LUMINOSOS'),
            ('4.3.A.1', 'SERVICIOS DE ALUMBRADO PÚBLICO'),
            ('4.3.B.1', 'SERVICIO DE AGUA POTABLE'),
            ('4.3.B.2', 'CONEXIONES Y RECONEXIONES'),
            ('4.3.B.3', 'DRENAJE Y ALCANTARILLADO'),
            ('4.3.B.4', 'ADEUDOS D/LOS SERV. D/SUM. D/AGUA POT.'),
            ('4.3.B.5', 'MANTENIMIENTO A LA RED DE AGUA POTABLE'),
            ('4.3.B.6', 'MANTENIMIENTO A LA RED D/DRENAJE Y ALC.'),
            ('4.3.B.7', 'PRESTACIÓN DE SERVICIOS DE ASIST. SOCIAL'),
            ('4.3.B.8', 'FERIAS MUNICIPALES'),
            ('4.3.C.1', 'SERVICIOS EDUCATIVOS Y OTROS'),
            ('4.3.C.2', 'COLEGIATURAS'),
            ('4.3.C.3', 'CURSOS'),
            ('4.4', 'OTROS DERECHOS'),
            ('4.4.1', 'OTROS DERECHOS'),
            ('4.5', 'ACCESORIOS DE DERECHOS'),
            ('4.5.1', 'RECARGOS'),
            ('4.5.1.1', 'RECARGOS POR DERECHO DE AGUA'),
            ('4.5.2', 'MULTAS'),
            ('4.5.2.1', 'MULTAS POR DERECHOS DE AGUA'),
            ('4.5.2.2', 'MULTAS OTROS'),
            ('4.5.3', 'ACTUALIZACIÓN'),
            ('4.5.3.1', 'ACTUALIZACIÓN POR DERECHOS DE AGUA'),
            ('4.5.3.2', 'ACTUALIZACIÓN OTROS'),
            ('4.9', 'DERECHOS NO COMP. EN LA LEY DE ING. VIG.'),
            ('4.9.1', 'PAGO'),
            ('5', 'PRODUCTOS'),
            ('5.1', 'USO O APROV. DE ESPACIOS EN EL MERCADO'),
            ('5.1.1', 'MERCADOS'),
            ('5.1.1.1', 'EXPLOTACIÓN DE OTROS BIENES'),
            ('5.1.1.2', 'USO O APROV. D/BIENES MUEB. E INMUEB.'),
            ('5.1.2', 'INGRESOS DE CAMIONES'),
            ('5.1.2.1', 'INGRESOS DE FOTOCOPIADO'),
            ('5.1.2.2', 'MAQUINARIA PESADA'),
            ('5.1.2.3', 'ESTACIONAMIENTO'),
            ('5.1.2.4', 'AUDITORIO MUNICIPAL'),
            ('5.1.2.5', 'ARRENDAMIENTO DE LOCALES'),
            ('5.1.2.6', 'BAÑOS PÚBLICOS'),
            ('5.1.2.7', 'ASIGNACIÓN DE LOTES EN CEMENTERIO'),
            ('5.1.2.8', 'EXPLOTACIÓN DE MAT. PETREOS Y CANTERAS'),
            ('5.1.2.9', 'INTERESES BANCARIOS, CRÉDITOS Y BONOS'),
            ('5.1.3', 'OTROS PRODUCTOS'),
            ('5.1.3.1', 'OTROS PRODUCTOS'),
            ('5.1.4', 'ACCESORIOS'),
            ('5.3.3.1', 'RECARGOS'),
            ('5.3.3.1.1', 'RECARGOS'),
            ('5.3.2', 'MULTAS'),
            ('5.3.2.1', 'MULTAS'),
            ('5.3.2.3', 'ACTUALIZACIÓN'),
            ('5.3.3.1', 'ACTUALIZACIÓN'),
            ('5.9', 'PRODUCTOS NO COMP. EN LA LEY DE ING. VIGENTE CAUS. EN EJER. FISC. ANT. PEND. DE LIO. O PAGO'),
            ('5.9.1', 'PRODUCTOS NO COMP. E/LA LEY D/INGRESOS'),
            ('6', 'APROVECHAMIENTOS'),
            ('6.1', 'APROVECHAMIENTOS'),
            ('6.1.1', 'RECARGOS'),
            ('6.1.1.1', 'RECARGOS'),
            ('6.1.2', 'MULTAS'),
            ('6.1.2.1', 'MULTAS'),
            ('6.1.3', 'ACTUALIZACIÓN'),
            ('6.1.3.1', 'ACTUALIZACIÓN'),
            ('6.1.4', 'GASTOS DE EJECUCIÓN'),
            ('6.1.4.1', 'GASTOS DE EJECUCIÓN'),
            ('6.1.5', 'HERENCIAS Y DONACIONES'),
            ('6.1.5.1', 'HERENCIAS Y DONACIONES'),
            ('6.1.6', 'SUBSIDIOS'),
            ('6.1.6.1', 'SUBSIDIOS'),
            ('6.1.7', 'INDEMNIZACIONES'),
            ('6.1.7.1', 'INDEMNIZACIONES'),
            ('6.1.8', 'INGRESOS DERIV. FINANC.O ORG. DESC.'),
            ('6.1.9', 'FIANZAS'),
            ('6.1.9.1', 'FIANZAS'),
            ('6.2', 'CONMUTACIONES'),
            ('6.2.1', 'APROVECHAMIENTOS PATRIMONIALES'),
            ('6.2.1.1', 'APROVECHAMIENTOS DE CAPITAL'),
            ('6.3', 'ACCESORIOS DE APROVECHAMIENTOS'),
            ('6.9', 'APROVECHA. NO COMP. EN LA LEY DE ING. VIGENTE CAUS. EN EJER. FISC. ANT. PEND. DE LIO. O PAGO'),
            ('6.9.1', 'APROVECHAM. NO COMP. E/LA LEY D/INGRESOS'),
            ('7', 'INGRESOS POR VENTAS DE BIENES, PRESTACIÓN DE SERVICIOS Y OTROS INGRESOS'),
            ('7.1', 'INGRESOS POR VENTA DE BIENES Y PRESTACIÓN DE SERVICIOS DE INSTITUCIONES PÚBLICAS DE SEGURIDAD SOCIAL'),
            ('7.1.1', 'INGR. P/VTAS DE B Y S D/ORG. DESC.'),
            ('7.2', 'INGRESOS POR VENTA DE BIENES Y PRESTACIÓN DE SERVICIOS DF EMPRESAS PRODUCTIVAS DEL ESTADO'),
            ('7.2.1', 'INGR. D/OPER. D/ENTID. PARAEST. EMPRES.'),
            ('7.3', 'INGRESOS POR VENTA DE BIENES Y PRESTACIÓN DE SERV. DE ENT. PARAEST. Y FIDIC. NO EMPR Y NO FINANC.'),
            ('7.3.1', 'INGR. VTAS D/B Y S PROD. ESTAB. GOB.CTRAL'),
            ('7.4', 'INGRESOS POR VENTA DE BIENES Y PRESTACIÓN DE SERV. DE ENT. PARAEST. EMPR NO FINANC. C/ PART. EST. MAY.'),
            ('7.5', 'INGRESOS POR VENTA DE BIENES Y PRESTACIÓN DE SERV. DE ENT. PARAEST. EMPR FIN. MONET C/ PART. EST. MAY'),
            ('7.6', 'INGRESOS POR VENTA DE BIENES Y PREST. DE SERV. DE ENT. PARAEST. EMPR FIN. NO MONET C/ PART. EST. MAY'),
            ('7.7', 'INGRESOS POR VENTA DE BIENES Y PREST. DE SERV. DE FIDEC. FINANC. PUBL. C/ PART. EST. MAY'),
            ('7.8', 'INGRESOS POR VENTA DE BIENES Y PREST. DE SERV. DE LOS PODERES LEG. Y JUD. Y ORG. AUTÓNOMOS'),
            ('7.9', 'OTROS INGRESOS'),
            ('8', 'PARTICIPACIONES, APORTACIONES, CONVENIOS, INCENTIVOS DERIV. DE LA COLAB. FISCAL Y FONDOS DIST. DE APORT'),
            ('8.1', 'PARTICIPACIONES'),
            ('8.1.1', 'FONDO GENERAL DE PARTICIPACIONES'),
            ('8.1.1.1', 'FONDO DE FOMENTO MUNICIPAL'),
            ('8.1.1.2', 'FONDO DE FISCALIZACIÓN Y RECAUDACIÓN'),
            ('8.1.1.3', 'FONDO DE COMPENSACIÓN'),
            ('8.1.1.4', 'FONDO DE EXTRACCIÓN DE HIDROCARBUROS'),
            ('8.1.1.5', 'IMPUESTO ESPECIAL SOBRE PRODUCCIÓN Y SERVICIOS'),
            ('8.1.1.6', '0.136% DE LA RECAUDACIÓN FEDERAL PARTICIPABLE'),
            ('8.1.1.7', '3.17% SOBRE EXTRACCIÓN DE PETRÓLEO'),
            ('8.1.1.8', 'FONDO DEL IMPUESTO SOBRE LA RENTA'),
            ('8.1.1.9', 'FONDO DE ESTABILIZACIÓN DE LOS INGRESOS DE LAS ENTIDADES FEDERATIVAS'),
            ('8.1.2', 'APORTACIONES'),
            ('8.1.2.1', 'FONDO DE APORTACIONES PARA LA NÓMINA EDUCATIVA Y GASTO OPERATIVO'),
            ('8.1.2.2', 'FONDO DE APORTACIONES PARA LOS SERVICIOS DE SALUD'),
            ('8.1.2.3', 'FONDO DE APORTACIONES PARA LA INFRAESTRUCTURA SOCIAL'),
            ('8.1.2.4', 'FONDO DE APORTACIONES PARA EL FORTALECIMIENTO DE LOS MUNICIPIOS'),
            ('8.1.2.5', 'FONDO DE APORTACIONES MÚLTIPLES'),
            ('8.1.2.6', 'FONDO DE APORTACIONES PARA LA EDUCACIÓN TECNOLÓGICA Y DE ADULTOS'),
            ('8.1.2.7', 'FONDO DE APORTACIONES PARA LA SEGURIDAD PÚBLICA DE LOS ESTADOS Y DEL DISTRITO FEDERAL'),
            ('8.1.2.8', 'FONDO DE APORTACIONES PARA EL FORTALECIMIENTO DE LAS ENTIDADES FEDERATIVAS'),
            ('8.3', 'CONVENIOS'),
            ('8.3.1', 'CONVENIOS DE PROTECCIÓN SOCIAL EN SALUD'),
            ('8.3.2', 'CONVENIOS DE DESCENTRALIZACIÓN'),
            ('8.3.3', 'CONVENIOS DE REASIGNACIÓN'),
            ('8.3.4', 'OTROS CONVENIOS Y SUBSIDIOS'),
            ('8.4', 'INCENTIVOS DERIVADOS DE LA COLABORACIÓN FISCAL'),
            ('8.4.1', 'TENENCIA O USO DE VEHÍCULOS'),
            ('8.4.1.1', 'FONDO DE COMPENSACIÓN ISAN'),
            ('8.4.1.2', 'IMPUESTO SOBRE AUTOMÓVILES NUEVOS'),
            ('8.4.1.3', 'FONDO DE COMPENSACIÓN DE RECURSOS INTERMEDIOS'),
            ('8.4.5', 'OTROS INCENTIVOS ECONÓMICOS'),
            ('8.5', 'FONDOS DISTINTOS DE APORTACIONES'),
            ('8.5.1', 'FONDO PARA ENTIDADES FEDERATIVAS Y MUNICIPIOS PRODUCTORES DE HIDROCARBUROS'),
            ('8.5.2', 'FONDO MINERO'),
            ('9', 'TRANSFERENCIAS, ASIGNACIONES, SUBSIDIOS Y SUBVENCIONES, Y PENSIONES Y JUBILACIONES'),
            ('9.1', 'TRANSFERENCIAS Y ASIGNACIONES'),
            ('9.1.1', 'TRANSF. INTERNAS Y ASIG. A/SECTOR PÚB.'),
            ('9.3', 'SUBSIDIOS Y SUBVENCIONES'),
            ('9.3.1', 'SUBSIDIOS Y SUBVENCIONES'),
            ('9.3.1.1', 'SUBSIDIOS Y SUBVENCIONES'),
            ('9.5', 'PENSIONES Y JUBILACIONES'),
            ('9.5.1', 'PENSIONES Y JUBILACIONES'),
            ('9.7', 'TRANSFERENCIAS DEL FONDO MEXICANO DEL PETRÓLEO PARA LA ESTABILIZACIÓN Y EL DESARROLLO')

        ]

        for codigo, descripcion in datos_servicios:
            servicio, created = Servicios.objects.get_or_create(
                codigoServicio=codigo,
                descripcion=descripcion
            )
            if created:
                self.stdout.write(f'Servicio creado: {codigo} - {descripcion}')
            else:
                self.stdout.write(f'Servicio ya existía: {codigo} - {descripcion}')

    def importar_codigos_postales(self):
        call_command('importpostalcodesmx')

    def crear_usuario_admin(self):
        municipio_chiautempan = Municipio.objects.filter(nombre="Chiautempan").first()
        if municipio_chiautempan:
            admin_user, created = CustomUser.objects.get_or_create(
                username='admin',
                defaults={
                    'password': make_password('12345'),
                    'Municipio': municipio_chiautempan,
                    'es_responsable': True,
                    'first_name': 'Juan',
                    'last_name': 'Ramos',
                    'apellido_materno': 'Ramos',
                    'email': 'juan.rr@apizaco.tecnm.mx', 
                    'is_superuser': True,  
                    'is_staff': True  
                }
            )
            if created:
                self.stdout.write("Usuario 'admin' creado exitosamente como superusuario.")
            else:
                self.stdout.write("Usuario 'admin' ya existía.")
                admin_user.email = 'juan.rr@apizaco.tecnm.mx'
                admin_user.is_superuser = True
                admin_user.is_staff = True
                admin_user.save() 
        else:
            self.stdout.write("Municipio 'Chiautempan' no encontrado. No se creó el usuario 'admin'.")