from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.model_general_information import GeneralInformation
from app.models.model_financial_information import FinancialInformation
from app.models.model_health_safety_requirements import HealthSafetyRequirements
from app.models.model_info_share_composition import InfoShareComposition
from app.models.model_legal_person import LegalPerson
from app.models.model_legal_representative_information import LegalRepresentativeInformation
from app.models.model_natural_person import NaturalPerson
from app.models.model_occupational_health_safety_requirements import OccupationalHealthSafetyRequirements
from app.models.model_references import References
from app.models.model_required_documents import RequiredDocuments
from app.models.model_tax_fiscal_information import TaxFiscalInformation
from app.models.model_authorizations_policies import AuthorizationsPolicies


async def post_form_supplier_db(db: Session, form_data, user_id):

    try:
        new_general_info = GeneralInformation(
            user_id=user_id,
            date_information=form_data.date_information,
            city_id=form_data.city_id,
            office_id=form_data.office_id,
        )

        new_natural = NaturalPerson(
            user_id=user_id,
            type_document_id=form_data.identification_type_id,
            municipality_id=form_data.municipality_id,
            region_id=form_data.region_id,
            country_id=form_data.country_id,
            name=form_data.name,
            last_name=form_data.last_name,
            document=form_data.document,
            expedition_date=form_data.expedition_date,
            birth_date=form_data.birth_date,
            address=form_data.address,
            zone=form_data.zone,
            email=form_data.email,
            phone=form_data.phone,
            company_name=form_data.company_name,
            nit=form_data.nit,
            occupation=form_data.occupation,
            monthly_income=form_data.monthly_income,
            other_income=form_data.other_income,
            specify=form_data.specify,
        )

        # Flush LegalPerson first to obtain its PK for dependent records
        new_legal = LegalPerson(
            user_id=user_id,
            reason_or_name=form_data.reason_or_name,
            nit=form_data.nit,
            address=form_data.address,
            region_id=form_data.region_id,
            city_id=form_data.city_id,
            society_type=form_data.society_type,
            link_type=form_data.link_type,
            municipality_id=form_data.municipality_id,
        )
        db.add(new_legal)
        db.flush()

        new_rep = LegalRepresentativeInformation(
            user_id=user_id,
            legal_person_id=new_legal.id_legal_person,
            name=form_data.rep_name,
            last_name=form_data.rep_last_name,
            document=form_data.rep_document,
            city_id=form_data.rep_city_id,
            phone=form_data.rep_phone,
            email=form_data.rep_email,
        )

        new_share = InfoShareComposition(
            user_id=user_id,
            legal_person_id=new_legal.id_legal_person,
            identification_type=form_data.identification_type,
            numero_identification=form_data.numero_identification,
            social_reason=form_data.share_social_reason,
            full_name=form_data.full_name,
            percentage=form_data.percentage,
        )

        new_tax = TaxFiscalInformation(
            user_id=user_id,
            common=form_data.common,
            big_taxpayer=form_data.big_taxpayer,
            simplified_regime=form_data.simplified_regime,
            self_retained_resolution=form_data.self_retained_resolution,
            self_retained_date=form_data.self_retained_date,
            big_taxpayer_resolution=form_data.big_taxpayer_resolution,
            big_taxpayer_date=form_data.big_taxpayer_date,
            self_retained_ica_resolution=form_data.self_retained_ica_resolution,
            self_retained_ica_date=form_data.self_retained_ica_date,
        )

        new_financial = FinancialInformation(
            user_id=user_id,
            total_active=form_data.total_active,
            total_passive=form_data.total_passive,
            patrimony=form_data.patrimony,
            monthly_income=form_data.monthly_income,
            monthly_expenditure=form_data.monthly_expenditure,
        )

        new_ref = References(
            user_id=user_id,
            bank_name=form_data.bank_name,
            titular_name=form_data.titular_name,
            number_telephone=form_data.ref_phone,
            address=form_data.ref_address,
            account_type=form_data.account_type,
            social_reason=form_data.ref_social_reason,
        )

        new_ohs = OccupationalHealthSafetyRequirements(
            user_id=user_id,
            document=form_data.ohs_document,
            fulfilled=form_data.ohs_fulfilled,
            observation=form_data.ohs_observation,
        )

        new_hs = HealthSafetyRequirements(
            user_id=user_id,
            document=form_data.hs_document,
            fulfilled=form_data.hs_fulfilled,
            observation=form_data.hs_observation,
        )

        new_auth = AuthorizationsPolicies(
            user_id=user_id,
            document_number=form_data.auth_document_number,
            expedition_place=form_data.auth_expedition_place,
            acting_as=form_data.auth_acting_as,
            ciiu_code=form_data.auth_ciiu_code,
            economic_activity=form_data.auth_economic_activity,
            licit_origin=form_data.auth_licit_origin,
            knowledge_normativity=form_data.auth_knowledge_normativity,
            no_third_party_deposits=form_data.auth_no_third_party_deposits,
            reality_statement=form_data.auth_reality_statement,
            sagrilat_verification=form_data.auth_sagrilat_verification,
            public_resources=form_data.auth_public_resources,
            public_power=form_data.auth_public_power,
            public_recognition=form_data.auth_public_recognition,
            pep_link=form_data.auth_pep_link,
            pep_position=form_data.auth_pep_position,
            pep_link_date=form_data.auth_pep_link_date,
            authorize_restrictive_lists=form_data.auth_authorize_restrictive_lists,
            policy_adherence=form_data.auth_policy_adherence,
        )

        records = [
            new_general_info,
            new_natural,
            new_tax,
            new_financial,
            new_rep,
            new_ref,
            new_share,
            new_ohs,
            new_hs,
            new_auth,
        ]

        if form_data.document_name:
            records.append(RequiredDocuments(
                user_id=user_id,
                document_name=form_data.document_name,
                is_verified=form_data.is_verified,
            ))

        db.add_all(records)
        db.commit()
        return "Formulario de proveedor guardado exitosamente"

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar el formulario: {str(e)}")
