module Documents.Decoder exposing (..)

import Date
import Documents.Company.Model as CompanyModel
import Documents.Inputs.Update as InputsUpdate
import Documents.Model exposing (Model, Document, Results, results)
import Documents.Receipt.Decoder as ReceiptDecoder
import Documents.SameDay.Model as SameDay
import Internationalization exposing (Language)
import Json.Decode exposing (Decoder, andThen, bool, float, int, keyValuePairs, list, nullable, string)
import Json.Decode.Pipeline exposing (decode, hardcoded, required)
import String


{-| From a query list of key/values get the page number:

    >>> getPage [ ( "page", "42" ), ( "year", "2016" ) ]
    Just 42

    >>> getPage [ ( "page", "foo bar" ) ]
    Nothing

    >>> getPage [ ( "format", "json" ) ]
    Nothing

-}
getPage : List ( String, String ) -> Maybe Int
getPage query =
    let
        tuple =
            List.head <|
                List.filter
                    (\( name, value ) ->
                        if name == "page" then
                            True
                        else
                            False
                    )
                    query
    in
        case tuple of
            Just ( name, value ) ->
                case String.toInt value of
                    Ok num ->
                        Just num

                    Err e ->
                        Nothing

            Nothing ->
                Nothing


dateInBrazil : String -> Decoder Date.Date
dateInBrazil str =
    let
        withTimezone : String
        withTimezone =
            if String.length str == 10 then
                str ++ "T12:00:00-03:00"
            else
                str
    in
        case Date.fromString withTimezone of
            Ok date ->
                Json.Decode.succeed date

            Err error ->
                Json.Decode.fail error


decoder : Language -> String -> List ( String, String ) -> Decoder Results
decoder lang apiKey query =
    let
        current =
            Maybe.withDefault 1 (getPage query)
    in
        decode Results
            |> required "results" (list <| singleDecoder lang apiKey)
            |> required "count" (nullable int)
            |> required "previous" (nullable string)
            |> required "next" (nullable string)
            |> hardcoded Nothing
            |> hardcoded current
            |> hardcoded ""


singleDecoder : Language -> String -> Decoder Document
singleDecoder lang apiKey =
    let
        supplier =
            CompanyModel.model
    in
        decode Document
            |> required "year" int
            |> required "document_id" int
            |> required "applicant_id" int
            |> required "total_reimbursement_value" (nullable float)
            |> required "total_net_value" float
            |> required "all_reimbursement_numbers" (list int)
            |> required "all_net_values" (list float)
            |> required "congressperson_id" (nullable int)
            |> required "congressperson_name" (nullable string)
            |> required "congressperson_document" (nullable int)
            |> required "state" (nullable string)
            |> required "party" (nullable string)
            |> required "term_id" int
            |> required "term" int
            |> required "subquota_id" int
            |> required "subquota_description" string
            |> required "subquota_group_id" (nullable int)
            |> required "subquota_group_description" (nullable string)
            |> required "supplier" string
            |> required "cnpj_cpf" (nullable string)
            |> required "document_type" int
            |> required "document_number" (nullable string)
            |> required "document_value" float
            |> required "issue_date" (string |> andThen dateInBrazil)
            |> required "month" int
            |> required "remark_value" (nullable float)
            |> required "installment" (nullable int)
            |> required "batch_number" (nullable int)
            |> required "all_reimbursement_values" (nullable <| list float)
            |> required "passenger" (nullable string)
            |> required "leg_of_the_trip" (nullable string)
            |> required "probability" (nullable float)
            |> required "suspicions" (nullable <| keyValuePairs bool)
            |> required "receipt" (ReceiptDecoder.decoder lang)
            |> hardcoded { supplier | googleStreetViewApiKey = apiKey }
            |> hardcoded SameDay.model


updateDocumentLanguage : Language -> Document -> Document
updateDocumentLanguage lang document =
    let
        receipt =
            document.receipt

        newReceipt =
            { receipt | lang = lang }

        supplier =
            document.supplierInfo

        newCompany =
            { supplier | lang = lang }
    in
        { document | receipt = newReceipt, supplierInfo = newCompany }


updateLanguage : Language -> Model -> Model
updateLanguage lang model =
    let
        results =
            model.results

        newDocuments =
            List.map (updateDocumentLanguage lang) model.results.documents

        newResults =
            { results | documents = newDocuments }

        newInputs =
            InputsUpdate.updateLanguage lang model.inputs
    in
        { model | lang = lang, inputs = newInputs, results = newResults }


updateGoogleStreetViewApiKey : String -> Model -> Model
updateGoogleStreetViewApiKey key model =
    { model | googleStreetViewApiKey = key }
