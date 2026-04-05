/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/14 15:38:02 by tsellak           #+#    #+#             */
/*   Updated: 2025/11/17 16:48:18 by tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static int	ft_conversions(char single, va_list arg)
{
	if (single == 'c')
		return (ft_print_char(va_arg(arg, int)));
	else if (single == 's')
		return (ft_print_str(va_arg(arg, char *)));
	else if (single == 'p')
		return (ft_print_ptr(va_arg(arg, unsigned long long)));
	else if (single == 'd' || single == 'i')
		return (ft_print_deci(va_arg(arg, int)));
	else if (single == 'u')
		return (ft_print_unsigned(va_arg(arg, unsigned int)));
	else if (single == 'x')
		return (ft_print_hex(va_arg(arg, unsigned int), 'x'));
	else if (single == 'X')
		return (ft_print_hex(va_arg(arg, unsigned int), 'X'));
	else if (single == '%')
		return (ft_print_char('%'));
	else
		return (ft_print_char(single));
}

int	ft_printf(const char *format, ...)
{
	va_list	arg;
	int		i;
	int		len;

	i = 0;
	len = 0;
	va_start(arg, format);
	if (!format)
		return (-1);
	while (format[i])
	{
		if (format[i] == '%')
		{
			if (format[i + 1] == '\0')
				return (-1);
			len += ft_conversions(format[i + 1], arg);
			i++;
		}
		else
			len += ft_print_char(format[i]);
		i++;
	}
	va_end(arg);
	return (len);
}
