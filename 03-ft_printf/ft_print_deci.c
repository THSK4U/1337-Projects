/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_deci.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/14 15:38:13 by tsellak           #+#    #+#             */
/*   Updated: 2025/11/14 15:38:14 by tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_print_deci(int n)
{
	int				len;
	unsigned int	num;

	len = 0;
	if (n < 0)
	{
		len += ft_print_char('-');
		num = (unsigned int)(-n);
	}
	else
		num = (unsigned int)n;
	if (num >= 10)
		len += ft_print_deci(num / 10);
	len += ft_print_char("0123456789"[num % 10]);
	return (len);
}
