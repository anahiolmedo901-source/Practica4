"""Cliente mínimo para NumberConversion SOAP con destino fijo y timeout."""

from urllib.error import URLError
from urllib.request import Request, urlopen
from xml.etree import ElementTree


SOAP_ENDPOINT = 'https://www.dataaccess.com/webservicesserver/NumberConversion.wso'
SOAP_ACTION = 'http://www.dataaccess.com/webservicesserver/NumberToWords'
SERVICE_NAMESPACE = 'http://www.dataaccess.com/webservicesserver/'
SOAP_NAMESPACE = 'http://schemas.xmlsoap.org/soap/envelope/'


class SoapServiceError(Exception):
    """La llamada al servicio SOAP externo falló o devolvió una respuesta inválida."""


def number_to_words(number):
    envelope = ElementTree.Element(f'{{{SOAP_NAMESPACE}}}Envelope')
    body = ElementTree.SubElement(envelope, f'{{{SOAP_NAMESPACE}}}Body')
    operation = ElementTree.SubElement(body, f'{{{SERVICE_NAMESPACE}}}NumberToWords')
    ElementTree.SubElement(operation, f'{{{SERVICE_NAMESPACE}}}ubiNum').text = str(number)
    payload = ElementTree.tostring(envelope, encoding='utf-8', xml_declaration=True)
    request = Request(
        SOAP_ENDPOINT,
        data=payload,
        headers={
            'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction': SOAP_ACTION,
            'Accept': 'text/xml',
        },
        method='POST',
    )

    try:
        with urlopen(request, timeout=10) as response:
            response_body = response.read(512_001)
    except (URLError, TimeoutError, OSError) as error:
        raise SoapServiceError('El servicio SOAP no está disponible.') from error

    if len(response_body) > 512_000:
        raise SoapServiceError('La respuesta del servicio SOAP excedió el tamaño permitido.')

    try:
        root = ElementTree.fromstring(response_body)
    except ElementTree.ParseError as error:
        raise SoapServiceError('El servicio SOAP devolvió XML no válido.') from error

    result = root.find('.//{*}NumberToWordsResult')
    if result is None or result.text is None:
        fault = root.find('.//{*}faultstring')
        message = fault.text if fault is not None and fault.text else 'Respuesta SOAP sin resultado.'
        raise SoapServiceError(message)
    return result.text
